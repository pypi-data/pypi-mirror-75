import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp as ivp
from scipy import interpolate
from scipy.optimize import minimize

class deltaMethod2():
    """
    Serves as an interface to the [deltaMethodUI] to implement the Approximate Delta Method [McB05].
    
    Notes/Issues:
        1. Most issues noted at method level docstrings
        2. Import statements - it seems that I need to import libraries at the method level.
           Why can't I import a library at the class level (as below) and have those available
           to each method? Moreover, this does seem to work, but inconsistently - e.g., I had 
           to import numpy as np into def oxsat, but did not have to import pandas as pd into 
           def adm... Because I had imported pandas as pd to the notebook and it was available 
           in the namespace (or something like that)...
           UNRESOLVED
    """
    
    def __init__(self, srcDat):
        
        self.srcDat = srcDat
        self.siteInfo = srcDat['siteInfo']
        self.timeZone = srcDat['timezone']
        self.geography = srcDat['geography']
        self.data = srcDat['data']
        self.solarObserver = self.setSolarObserver()
        self.admResult = self.adm()
    
    def __str__(self):

        """
        Issues:
            1. TypeError: __str__ returned non-string (type NoneType)
               Tried to cast to string as shown below, no change in error.
               UNRESOLVED
        """
        siteInfo = self.siteInfo
        timeZone = self.timeZone
        geography = self.geography
        
        print('Instance of deltaMethod.')
        print('Site Information:'.format(siteInfo))
        print('TimeZone Information:'.format(timeZone))
        print('Geographic Information:'.format(geography))
        
    def oxsat(self, wtemp):
        
        """
        Calculates the dissolved oxygen saturation (mg/L)
        following APHA Standard Methods[1]

        Args:
            wtemp = water temperature in degrees celsius
            elev = elevation in meters above sea level

        Returns:
            osat = oxygen saturation in mg/L

        Notes:
            1. Update with new equations from SC
                a. Updated, seems to reduce performance (shouldn't)
                
        References:
            1. Chapra & Camacho, 2020
            2. APHA 1995
            3. Zison et al., 1978
        """
        
        # compute elevation above sea level (km)
        elev = self.geography['navd88_m']/1000
        # compute absolute temperature 
        Taa = wtemp + 273.15
        
        # compute ln(oxygen saturation at sea level) (APHA 1995)
        lnosf = -139.34411 + 157570.1/Taa - 66423080/Taa**2
        lnosf = lnosf + 12438000000/Taa**3 - 862194900000/Taa**4
        
        # old way (Zizon et al, 1978)
#         osat = np.exp(lnosf)*(1 - 0.0001148*elev)
        
        # new way (Chapra & Camacho, 2020)
        oss = np.exp(lnosf)
        osz = oss*(1-0.11988*elev + 6.10834e-3*elev**2\
                   - 1.60747e-4*elev**3)
        
        return osz
    
    def setSolarObserver(self):
        
        """
        Creates an observer object for use with the solar calculator,
        utilizing AstroPy and the site geographic data.
        
        Returns:
            Sets the solarObserver attribute for the deltaMethod instance.
        
        References: 
            https://pypi.org/project/astroplan/
            
        Notes/Issues:
            1. IERS methods employed below should be done only on application 
               start-up/delta2k import. Need to figure out how best to do this.
               Probably a `startUp` module that is run directly after import...
               UNRESOLVED
               
            2. IERS tables need to be refreshed regularly (thus the start-up
               module proposed above), but the download service is unstable, 
               and fatal if unsuccessful. Need to figure out a try/ex to 
               increase stability - the improved accuracy of the IERS updates
               is nice, but not a must for the precision required in this 
               particular application (affects cosmoogical observations more
               than near-Earth observations like sunrise/noon/set).
               Issue References:
                   https://docs.astropy.org/en/stable/utils/iers.html
                   https://github.com/astropy/astropy/issues/9499
               UNRESOLVED
               
            3. The timezone argument is required but seems to be constrained to 
               string-based representations. Hopefully Astroplan has a means of
               avoiding this by staying in UTC. Need to do more research on this 
               to confirm solution.
               UNRESOLVED
                
        """
        print("Creating observation point for solar geometry.")
        # Local imports
        from astropy.utils import iers
        from astropy.utils.iers import conf as iers_conf
        from astroplan import download_IERS_A
        from astropy.coordinates import EarthLocation
        import astropy.units as u
        from astroplan import Observer
        from astropy.time import Time
        
        # Issue 2 resolution  - move to startUp when available
        #____________________________________________________#
        # try to refresh IERS_A tables, pass any warnings
        try:
            download_IERS_A()
        except:
            pass

        # Establish an observer location 
        # define location parameters
        longitude = self.geography['longitude']
        latitude = self.geography['latitude']
        elevation = self.geography['grs80_m']
        
        loc = EarthLocation.from_geodetic(longitude*u.deg,
                                          latitude*u.deg,
                                          elevation*u.m)
        
        # create Observer object
        obs = Observer(location=loc,
                       name='obs',
                       # ISSUE: need to figure out how to 
                       # deal with UTC instead.
                       timezone='US/Eastern')
        
        # try to calculate sunrise and turn off IERS age
        # thresholds if exception occurs
        try: 
            date = Time.now()
            time = Time(date, location=obs.location)
            sr = obs.sun_rise_time(time,'next').iso
        
        except:
            # Nullify IERS age thresholds
            iers_conf.auto_max_age = None
            
            # Test resolution
            try:
                sr = obs.sun_rise_time(time,'next').iso
            except:
                print("Fatal error calculating sunrise. Unresolved issue.")
        return obs
                
    def solar(self, date):
        
        """
        Computes solar geometries required for the delta method,
        utilizing the AstroPlan package in AstroPy.
        
        Inputs:
            date = datetime object
            
        Returns:
            tuple(sunrise, solar noon, sunset)
            
        References:
            https://pypi.org/project/astroplan/
            
        Notes/Issues:
            1. Need to test timezone reliability.
               UNRESOLVED
            2. Need to add conversion from UTC to local
               using self.timezone.
               UNRESOLVED
        """
        from astropy.coordinates import EarthLocation
        from astropy.coordinates import EarthLocation
        import astropy.units as u
        from astroplan import Observer
        from astropy.time import Time
        
        obs = self.solarObserver
        time = Time(date, location=obs.location)
        sr_utc = obs.sun_rise_time(time,'next').iso
        sn_utc = obs.noon(time,'next').iso
        ss_utc = obs.sun_set_time(time,'next').iso
        return (sr_utc,sn_utc,ss_utc)
    
    def adm(self):
        """
        Implements the Approximate Delta Method [McB05] using 
        a split/apply/combine pattern on a source dataframe.
        
        Inputs:
        
        Returns:
            Sets the admResult attribute with the resulting dataframe
            for use in downstream processes.
            
        References:
            [McB05] - McBride and Chapra, 2005. The Approximate Delta Method.
            
        Notes/Issues:
            1. Need to add step to chop off partial days from self.data
               otherwise deltas cannot be calculated accurately.
               UNRESOLVED
            2. Computation of solar parameters may not be as efficient as
               possible. See note below in context.
               UNRESOLVED
            2. Complete definition
               UNRESOLVED
        """
        import pandas as pd
        
        df = self.data
        
        # check for NaNs in wtemp and do_mass
        ## replace QC values with 'd2k_interp' if nan
        ### interpolate NaNs
        cols = [i for i in self.data.columns]
        if 'qc_wtemp_c' in cols:
            # for NWIS
            self.data.qc_wtemp_c = self.data.qc_wtemp_c.fillna(value='d2k_interp')
            self.data.wtemp_c = self.data.wtemp_c.interpolate(method='time')
        else:
            # for local files
            self.data.assign(qc_wtemp_c = 'P')
            self.data.loc[self.data.wtemp_c.isna(), 'qc_wtemp_c'] = 'd2k_interp'
            self.data.wtemp_c = self.data.wtemp_c.interpolate(method='time')
        if 'qc_do_mass' in cols:
            # for NWIS
            self.data.qc_do_mass = self.data.qc_do_mass.fillna(value='d2k_interp')
            self.data.do_mass = self.data.do_mass.interpolate(method='time')
        else:
            # for local files
            self.data.assign(qc_do_mass = 'P')
            self.data.loc[self.data.do_mass.isna(), 'qc_do_mass'] = 'd2k_interp'
            self.data.do_mass = self.data.do_mass.interpolate(method='time')
        

        
        # OFI - rewrite below using pd.assign, merges not necessary
        #add osat to df
        self.data = self.data.assign(osat = self.oxsat(self.data.wtemp_c))
#         osat = pd.Series(self.oxsat(df.wtemp_c),name='osat')
#         df = pd.merge(df,osat,left_index=True,right_index=True)

        #add DO deficit to df 
        self.data = self.data.assign(deficit = self.data.osat-self.data.do_mass)
#         deficit = pd.Series(df.osat-df.do_mass,name='deficit')
#         df = pd.merge(df,deficit,left_index=True,right_index=True)

        print("Resampling data to daily values.")
        
        # remove QC fields (WHY?)
        cols = [i for i in self.data.columns if 'qc' not in str(i)]
        df = self.data[cols]
        
        # ISSUE 1 PLACEHOLDER
            # trim partial days from df
            # UNRESOLVED# split into daily subgroups
        days = df.resample('D')

        # apply daily summary statistics
        mindef = days.deficit.min()
        maxdef = days.deficit.max()
        meantemp = days.wtemp_c.mean()
        meandef = days.deficit.mean()

        # get times of daily extremes
#         timeMinDef = days.deficit.idxmin()
#         timeMaxDef = days.deficit.idxmax()
        # The above fails with resampled indexes where some days are missing
        ## unresolved bug in pandas - see 
        timeMinDef = df.deficit.resample('D').agg(lambda x: 
                        pd.to_datetime(str(x.idxmin()),utc=True).tz_convert(df.index[0].tz) if x.count() > 0 else np.nan)\
                       .dropna()
        timeMaxDef = df.deficit.resample('D').agg(lambda x: 
                        pd.to_datetime(str(x.idxmax()),utc=True).tz_convert(df.index[0].tz) if x.count() > 0 else np.nan)\
                       .dropna()
        # combine all together
        dfdaily = pd.merge(timeMaxDef,
                       pd.merge(timeMinDef,
                           pd.merge(meantemp,
                               pd.merge(maxdef,
                                    pd.merge(mindef,meandef,
                                     left_index=True,right_index=True),
                                left_index=True,right_index=True),
                           left_index=True,right_index=True),
                        left_index=True,right_index=True),
                   left_index=True,right_index=True)
        names = ['tmaxD','tminD','meanT','maxD','minD','meanD']
        dfdaily.columns = names
        
        # compute delta for each day
        delta = pd.Series(dfdaily.maxD-dfdaily.minD,name='delta')
        dfdaily = pd.merge(dfdaily,delta,left_index=True,right_index=True)
        
        # compute daily solar parameters
        # sunrise
        dfdaily = dfdaily.assign(sunrise=
            dfdaily.index.to_series().
                  apply(lambda x: 
                            pd.to_datetime(self.solar(x)[0],
                                           utc=True).
                                   tz_convert(x.tz)))
        # solnoon
        dfdaily = dfdaily.assign(solnoon=
            dfdaily.index.to_series().
                  apply(lambda x: 
                            pd.to_datetime(self.solar(x)[1],
                                           utc=True).
                                   tz_convert(x.tz)))
        # sunset
        dfdaily = dfdaily.assign(sunset=
            dfdaily.index.to_series().
                  apply(lambda x: 
                            pd.to_datetime(self.solar(x)[2],
                                           utc=True).
                                   tz_convert(x.tz)))
        # lag
        dfdaily = dfdaily.assign(lag= 
            (dfdaily.tminD-dfdaily.solnoon).
                apply(lambda x: 
                          x.total_seconds()/86400*24))
        # photoperiod
        dfdaily = dfdaily.assign(photo= 
            (dfdaily.sunset-dfdaily.sunrise).
                apply(lambda x: 
                          x.total_seconds()/86400*24))
        # eta
        dfdaily = dfdaily.assign(eta= 
            dfdaily.photo.
                apply(lambda x:
                         (x/14)**0.75))
        
        print("Computing approximate delta method for each day.")
        # filter down to data meeting delta method requirements
        dff = dfdaily[(dfdaily.lag > 0) & (dfdaily.tminD-dfdaily.index > pd.Timedelta(0))]

        # split data following delta method conditional logic
        dfcond1 = dff[5.3*dff.eta-dff.lag > 0]
        dfcond2 = dff[5.3*dff.eta-dff.lag <= 0]

        # apply delta method appropriate to each condition
        ka = pd.Series(7.5*((5.3*dfcond1.eta - dfcond1.lag)/dfcond1.eta/dfcond1.lag)**0.85,name='ka')
        katype = pd.Series(ka.index.to_series().apply(lambda _: "delta_method"),name='katype')
        ka = pd.merge(ka,katype,left_index=True,right_index=True)

        ka7 = pd.Series(dfcond2.meanD/dfcond2.meanD*7.0,name='ka')
        ka7type = pd.Series(ka7.index.to_series().apply(lambda _: "default7"),name='katype')
        ka7 = pd.merge(ka7,ka7type,left_index=True,right_index=True)

        kat = pd.concat((ka,ka7),sort=False).sort_index()

        # recombine data
        dff = pd.merge(dff,kat,left_index=True,right_index=True)

        # calculate primary production and merge into dff
        meanP = pd.Series(dff.eta*dff.delta/16*(33+dff.ka**1.5),name='meanP')
        dff = pd.merge(dff,meanP,left_index=True,right_index=True)

        # calculate primary respiration and merge into dff
        meanR = pd.Series(dff.meanP + dff.ka*dff.meanD, name='meanR')
        dfdelta = pd.merge(dff,meanR,left_index=True,right_index=True)
        
        print("Finished.")
        return dfdelta

    def arrh(self,k20,T,theta):
        """
        Returns a temperature corrected rate coefficient using 
        the simplified Arrhenius equation

        Args:
        k20 =   rate at 20 celsius
        T =     temperature of interest
        theta = temperature coefficient for reaction of interest
        """
        return k20*theta**(T-20)

    def photo(self,p,f,t,tsr,temp):
        """
        This is calculating photosynthetic oxygen prodcution for 
        the current timestep. If good solar data is available, this can
        be tweaked:
            Compute clear-sky radiation v time for day
                Ratio over course of day - fractionof ideal radiation, 
                goes in front of pmax (basically cloud-cover efficiency)

                Given time-series of ADM estimates, and this output, plot
                together and examine if approximation breaks down in a
                systematic manner. Claim is that you can use ADM in place
                of this method as quick estimate. 
        """
        pmax = p
        
        # if t in photoperiod
        if (t < tsr) | (t>tsr+f):
            p_t = 0
        else:
            p_t = pmax*1.066**(temp-20)*np.sin(np.pi*(t-tsr)/f)
        return p_t

    def derivs(self,t,c,temp_int,trise,f,est):

        """
        Calculates derivatives (dc/dt) for (t,c) over time period
        (tspan), taking into account water temperature using
        a PCHIP interpolator (temp_int), water depth (h), elevation of
        site (elev), time of sunrise (trise), duration of 
        photoperiod (f), and a vector (est) containing initial
        estimates for reaeration rate (/day), primary production
        (/day), and community respiration (/day).

        Returns:
        dc, the d(domass)/dt for time t
        """

        # interpolate temperature at t, calc DO saturation
        temp_t = temp_int(t)
        dosat = self.oxsat(temp_t)

        # unpack estimated values
        ka = est[0]
        p = est[1]
        r = est[2]

        # calculate rates at temp(t)
        ka_t = ka*1.024**(temp_t-20)
        r_t = r*1.07**(temp_t-20)

        # calculate photosynthesis at this time
        p_t = self.photo(p,f,t,trise,temp_t)

        # calculate net rate for this time step
        dc = np.zeros(1)
    #     dc[0] = ka_t*(dosat-c[0])+p_t-r_t
        dc = ka_t*(dosat-c)+p_t-r_t
    #     dc = dc.reshape((1,))

        return dc

    def residuals(self,est,temp_int,
                    trise,f,tspan,y0,
                    tdata,cdata,today):
        """
        Calculate the residual error betweent the concentrations
        predicted by integration (using first approximation from 
        ADM) and observed data. Results passed to 
        `scipy.least_squares` for optimization.
        """
        # compute solution with current estimate
        fit = ivp(lambda t,c:
                 self.derivs(t,c,temp_int,trise,f,est),
             tspan,
             y0,
             t_eval=tdata)
        cpred = fit.y.reshape(cdata.shape)
        
        # compute first objective residuals
        resid1 = cdata - cpred
        r1 = resid1**2
        r1 = r1.sum()
        
        # mean deficit objective residuals
        ka = est[0]
        maxP = est[1]
        R = est[2]
        meanP = maxP*2*f/np.pi
        meanD = self.admResult[self.admResult.index.date == today]['meanD']
        fitD = (R - meanP)/ka
        resid2 = meanD - fitD
        r2 = resid2**2
        r2 = r2.sum()
        
        # sum residuals
        r = r1 + r2
        return r.sum()

    def rpd(self,adm_est,fit_est):
        """
        Compute relative percent difference between initial and 
        fitted estimators.
        """
        avg = [(adm_est[i] + fit_est[i])/len(fit_est) for i in range(len(fit_est))]
        diff = fit_est - adm_est
        rpd = diff/avg
        return rpd

    def fitDay(self, fitdate, user_est, print_results):
        """
        Uses the admRes parameters to fit a mass-balance model for dissolved oxygen.

        srcDat = source data, instance of delta2k.sourceRequest.srcDat
        admRes = approximate delta method result, instance of delta2k.deltaMethod.admResult
        fitdate = the date to be used for the fit, pandas datetime object
        """
        dayspan = 86400000000000

        # create local aliases
        srcDat = self.srcDat
        admRes = self.admResult
        srcDf = srcDat['data']

        # get the requested date
        today = fitdate
        tomorrow = today + pd.to_timedelta(1,'D')

        # get the first observation on the next day to enable smooth fitting over days
        if tomorrow in admRes.index.date:
            srcDf = srcDf[(srcDf.index.date >= today) &
              (srcDf.index <= srcDf[srcDf.index.date == tomorrow].index[0])]
            lastDay = False
        else:
            srcDf = srcDf[srcDf.index.date == today]
            lastDay = True
        admDf = admRes[(admRes.index.date == today)]
        temp_obs = srcDf['wtemp_c']
        do_obs = srcDf['do_mass']

        # could this work over several days? still have to get trise/tset for each day...
        tdata = [(float(i.value) - temp_obs.index[0].value)/dayspan for i in temp_obs.index]

        # build pchip interpolator to pass to derivs
        temp_int = interpolate.PchipInterpolator(tdata, temp_obs.values)

        # get solar data from admResult
        trise = (float(int(admDf.sunrise.values[0])) - temp_obs.index[0].value)/dayspan
        tset = (float(int(admDf.sunset.values[0])) - temp_obs.index[0].value)/dayspan
        f = tset-trise

        # define inputs for fitsolver
        tspan = np.array([tdata[0],tdata[-1]])

        # use initial user-input estimates or use ADM estimates:
        if user_est is None:
            # using ADM estimates instead
            meanP = admDf.meanP[0]
            # @Chapra p.436
            maxP = meanP*np.pi/(2*f)
            meanR = admDf.meanR[0]
            ka = admDf.ka[0]
            est = np.array([ka, maxP, meanR])
        else: 
            est = user_est

        # initial conditions as 1D array
        do_init = admRes['fit_do_init'].values[0]
        y0 = [do_init]
        true_init_err = do_obs[0] - do_init

        # system
#         h = 3.0 # meters
        elev = srcDat['geography']['navd88_m']

        # Minimize the sum of squared residuals between
        # observed and predicted dissolved oxygen concentrations
        # by adjusting the three-parameter estimate of [ka, maxP, meanR]
        # as provided by the ADM result for each day (or by the user as an array)

        opt = minimize(self.residuals,est,
                            method='Nelder-Mead',
#                             method='Newton-CG',
#                             options={'maxiter': None, 'adaptive': True},
                            args=(temp_int,
                                trise,f,tspan,y0,
                                tdata,do_obs.values,
                                today))
        # Save the optimal fitted parameters
        fitEst = opt.x
        ka = fitEst[0]
        maxP = fitEst[1]
        R = fitEst[2]
        meanP = maxP*2*f/np.pi
        meanD = self.admResult[self.admResult.index.date == today]['meanD']
        fitD = (R - meanP)/ka

        # Run the mass balance model using the optimal parameters
        # And save the optimal result for output
        optFit = ivp(lambda t,c:
                 self.derivs(t,c,temp_int,trise,f,fitEst),
                 tspan,
                 y0,
                 t_eval=tdata,
                 vectorized=False)

        tOpt, cOpt = optFit.t, optFit.y
        cOpt = cOpt.reshape(tOpt.shape)

        # Update initial condition in admRes to final condition in prediction on this day
        # (to be used as initial condition on next day)
        admRes.loc[:,'fit_do_init'] = cOpt[-1]

        # Calculate RPD between initial estimate and fitted estimate
        rpd_est = self.rpd(est, fitEst)
        # Create output dictionary fitResult
        do_pred = pd.Series(data=cOpt,index=srcDf.index)
        if lastDay == False:
            do_pred = do_pred[:-1]

        fitResult = {'temp_obs': temp_obs,
                     'do_obs': do_obs,
                     'meanD': meanD,
                     'do_pred': do_pred,
                     'fit_ka': fitEst[0],
                     'fit_maxP': fitEst[1],
                     'fit_meanP': fitEst[1]*2*f/np.pi,
                     'fit_meanR': fitEst[2],
                     'fitD': fitD,
                     'opt': opt,
                     'rpd': rpd_est,
                     'true_init_err': true_init_err}
        
        if print_results:
            # Print the optimization result message and obj. fun result
            print("Date: {}".format(today))
            print("Optimization message: {}".format(opt.message))
            print("Sum of squared residuals: {}".format(opt.fun))
            print("Initial condition error: {}".format(true_init_err))
            print("Fitted estimates:\n\tReaeration: {}\n\tMax. Productivity: {}\n\tRespiration: {}"\
                  .format(fitEst[0], fitEst[1], fitEst[2]))

        return fitResult
    
    def fit2DO(self, user_est=None, print_results=False):
        # set initial conditions
        if 'fit_do_init' in self.admResult.columns:
            self.admResult['fit_do_init'] = self.srcDat['data']['do_mass'].values[0]
        else:
            self.admResult = self.admResult.assign(fit_do_init = self.srcDat['data']['do_mass'].values[0])

        # Update admResult with fitResult
        self.admResult = self.admResult\
        .assign(fitResult = self.admResult.index.to_series()\
                .apply(lambda x: self.fitDay(x.date(),user_est,print_results)))