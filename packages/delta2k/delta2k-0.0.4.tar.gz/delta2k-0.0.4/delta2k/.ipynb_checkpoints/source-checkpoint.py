# General modules
import numpy as np
import pandas as pd
import urllib
import json

# Scipy modules
import scipy
from scipy import optimize
from scipy.integrate import solve_ivp as ivp
from scipy import interpolate
from scipy.optimize import minimize

# Bokeh graphics modules
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, show
from bokeh.models import HoverTool
from bokeh.plotting import figure, ColumnDataSource

class source():
    
    """
    Interface for loading data for analysis via the Delta Method. 

    Example:
    myRequest = sourceRequest('NWIS', 
                        site='04208000',
                        service='iv',
                        period='P1D',
                        startDate = None,
                        endDate = None,
                        parameterCd = None)
    """
    
    def __init__(self, srcType, **kwargs):
        self.__src = ''
        self.__srcChk = ''
        self.__elevation = None
        self.geography = None
        self.timezone = None
        self.siteinfo = None
        self.data = None
        
        # common attributes
        if 'elevation' in kwargs:
            self.__elevation = kwargs['elevation']
            
        # NWIS attributes
        self.__nwis_site = '04208000'
        self.__nwis_svc = 'iv'
        self.__nwis_pd = 'P1D'
        self.__nwis_start = None
        self.__nwis_end = None
        self.__nwis_pcode = None
        self.__nwis_url = ''
        self.srcDat = None
        
        # Local attributes
        self.__file_path = None
        self.__columns = None
        self.__time_index = None
        self.__sep = None
        
        if srcType == 'NWIS':
            # assert site in kwargs
            self.__src = 'NWIS'
            self.__nwis_site = kwargs['site']
            if 'service' in kwargs.items():
                self.__nwis_svc = kwargs['service']
            else:
                self.__nwis_svc = 'iv'
            self.__nwis_pd = kwargs['period']
            self.__nwis_start = kwargs['startDate']
            self.__nwis_end = kwargs['endDate']
            if 'parameterCd' in kwargs.items():
                self.__nwis_pcode = kwargs['parameterCd']
            self.__urlChk = self.__nwisURL()
            print(self.__urlChk)
            if self.__urlChk[1] == True:
                self.__nwis_url = self.__urlChk[0]
                self.srcDat = self.__getNWIS()
#                 self.data = self.srcDat.copy()
        
        if srcType == 'local':
#             custer = sourceRequest('local',
#                       filepath = fileName,
#                       columns = columns,
#                       units = units,
#                       geog = geog,
#                       tz = tz)
            self.__src = 'local'
            self.__sep = kwargs['sep']
            self.__local_path = kwargs['path']
            self.__local_cols = kwargs['columns']
            self.__local_units = kwargs['units']
            self.siteinfo = kwargs['site']
            self.geography = kwargs['geography']
            self.timezone = kwargs['timezone']
            
            self.srcDat = self.__getLocal()
#             self.data = self.srcDat.copy()
            
            # continue ETL to sqlite
            # self.srcDat = self.__getLocal()
            
#         if self.srcDat != None:
            # check the format before saving to sqlite
            # save to sqlite
        self.__solarObserver = self.__setSolarObserver()
        self.admResult = self.__adm()
        # self.dataplot = None
        # self.resultplot = None
    
    def __str__(self):
        print('Instance of delta2k source request.')
        print('Source of data: {}'.format(self.__src))
        
    def __elevationTNM(self, longitude, latitude):
        """
        Queries The National Map elevation API. 
        Requests valid only in conterminous US. 
            Need to add try/ex to check for valid response:
                Except = User input: Invalid elevation received. Enter valid elevation for site...
        No data value = -1000000

        Inputs:
        longitude = NAD83, enter as negative
        latitude = NAD83
        
        Returns: 
        elev = elevation in NAVD88 feet
        
        References:
        http://nationalmap.gov/epqs
        
        Notes:
        TNM API became unstable as of (noticed on) 2020-05-09. Reference page has 
        disappeared. Added try/ex below which will always raise exception until
        USGS repairs page or advises on replacement service.
        
            Resolution: Unresolved.
        """
        
        try:
            nationalMap = 'https://nationalmap.gov/epqs/pqs.php?x={}&y={}&units=feet&output=json'.format(str(longitude),str(latitude),units)
            page = urllib.request.urlopen(nationalMap).read()
            response = json.loads(page)
            elev = response['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation']
        except:
            elev = input("The API did not return a valid elevation. Please enter a site elevation in NAVD88 feet to proceed:")
            elev = float(elev)
        return elev
        
    def __getGeoidHt(self, longitude, latitude):
        """
        Interface to NOAA Geodesy API to compute height above geoid at site.  
        Requests valid anywhere on Earth. 
        
        Inputs: 
        longitude = NAD83(2011)
        latitude = NAD83(2011)
        
        Returns:
        geoidHt = geoid height (meters) above (+)/below (-) NAD83 ellipsoid (aka GRS80) 
        
        References:
        https://www.ngs.noaa.gov/web_services/geoid.shtml
        
        Notes:
            1. NGS is planning to discontinue the GEOID models and upgrade to the North 
            American-Pacific Geopotential Datum of 2022 upon completion of that project. 
            This method will need to be updated at that time.
                - Unresolved
        """
        
        import urllib
        import json
        
        geodesyURL = 'https://geodesy.noaa.gov/api/geoid/ght?lat={}&lon={}'.format(latitude,longitude)
        page = urllib.request.urlopen(geodesyURL).read()
        ght = json.loads(page)['geoidHeight']
        
        return ght
        
    def __grs80(self, longitude, latitude, navd88_m):
        """
        Implements getElevationTNM and getGeodesy to retrieve
        site elevation from The National Map and convert to 
        GRS80 ellipsoid height using getGeodesy to request 
        geoid height at location.
        
        Inputs:
        longitude = NAD83(2011)
        latitude = NAD83(2011)
        elevation = NAVD88 feet, optional override of lat/lon API methods
                    If used, user elevation is converted to GRS80 for 
                    downstream requirements.
        
        Returns:
        grs80_m = the approximate elevation (meters) of the site above 
                  the GRS80 ellipsoid.
        
        References:
        https://earth-info.nga.mil/GandG/publications/vertdatum.html
        
        Notes:
        """

        geoidHt_m = self.__getGeoidHt(longitude, latitude)
        grs80_m = navd88_m + geoidHt_m
        
        return (geoidHt_m, grs80_m)
        
    def __nwisURL(self):
        """
        Concatenates specified site, period and parameter data
        into a valid URL to the waterservices.usgs.gov REST API
        for instantaneous (high-frequency) values.

        Input:
            site = 8-character (string) numerical ID for USGS gauge, 
                as displayed at NWIS. This function only supports querying
                one site at a time, but future updates may support multi-site
                queries and multi-index dataframe generation for each site
                requested.

            period = backward-looking period over which to return data. Default is 
                one day. For sites with predictive models, this may return current 
                predictions into the future. Use only a positive ISO-8601 duration 
                format (https://en.wikipedia.org/wiki/ISO_8601#Durations).
                Bear in mind that there is latency between when a value is recorded 
                at the site and when it appears on the web, typically 0-4 hours. 

                Examples: 
                    'P2D' goes back two days from now
                    'PT4H' goes back four hours from now
                    'P2DT2H' (or 'PT50H') goes back 50 hours
                    'P1DT22H (or 'PT46H') goes back 46 hours from now

            startDate = Option to define a starting date. If chosen, an ending 
                date must be specified as well. Data is returned for the period
                from the start date to the end date. This over-rides the period 
                argument.

                Example:
                    startDate = '2020-03-06'
                    endDate = '2020-03-11'

            endDate = Ibid.

            parameterCd = list of site parameters to request. Default = None,
                which returns all available parameters. Passing a list will 
                over-ride this behavior and return only those requested. Enter 
                parameters as a list of string parameter codes separated by commas. 
                See 
                (https://help.waterdata.usgs.gov/codes-and-parameters/parameters)
                for a complete list. 

                Common values include:
                  stage (height in feet, gauge datum): enter '00060'
                  flow (cubic feet per second): enter '00065'
                  dissovled oxygen (mg/L): enter '00300'
                  water temperature (Celsius): enter '00010'

                Example: 
                    To request only dissolved oxygen and water termperature,
                    pass:
                        parameterCd = ('00300','00010')
                    To request only flow, pass:
                        parameterCd = ('00065')
        Returns:
            urlState, a list containing:
                [0] the truth value of the URL test which looks at the queryInfo type to 
                    ensure that it is a valid response from waterservices.usgs
                [1] the URL that was tested

        Example: Build URL for the Cuyahoga River at Independence, Ohio and request
            dissolved oxygen, temperature and flow rate for the period between 
            March 12, 2020 and March 13, 2020.

            params = ('00300','00010','00065')
            waterServicesURL(site='04208000',
                             startDate='2020-03-12',
                             endDate='2020-03-13',
                             parameterCd=params)
        
        Issues/Notes:
            1. Need to add conditional to URL creation for length of record requested.
                a. If request period is greater than 30 days, use gzip compression
                b. Otherwise proceed as written
                c. Or - is there any real performance loss to using gzip across the board?
        """
        print("Checking that URL is valid.")
        
        site = self.__nwis_site
        service= self.__nwis_svc
        period= self.__nwis_pd
        startDate = self.__nwis_start
        endDate = self.__nwis_end
        parameterCd = self.__nwis_pcode

        baseURL = 'http://waterservices.usgs.gov/nwis'
        fmt = '?format=json'
        # Handle period arguments:
        dateUsed = False
        dateCheck = (type(startDate), type(endDate))
        # if type[0] != type[1]
        # make much more...
            # assert
        if dateCheck == (type(None),type(None)):
            dateUsed = False
        if dateCheck == (str,str):
            dateUsed = True
            # might add errortrap here for heterogeneous type error...
            # 
        if dateUsed == True:
            period = 'startDT={}&endDT={}'.format(startDate,endDate)
        else:
            period = 'period={}'.format(period)

        # Handle parameter arguments:
        if parameterCd != None:
            parameterCd = "".join(
                                str([i for i in parameterCd])
                                .strip("[]")
                                .strip("'")
                                .split(" ")).replace("'","")
            parameterCd = 'parameterCd={}'.format(parameterCd)
        else:
            parameterCd = ''

        # Build full URL
        testURL = '{}/{}/{}&indent=on&sites={}&period=P1D&{}&siteStatus=all'.format(
                    baseURL,
                    service,
                    fmt,
                    site,
                    parameterCd)
        
        fullURL = '{}/{}/{}&indent=on&sites={}&{}&{}&siteStatus=all'.format(
                    baseURL,
                    service,
                    fmt,
                    site,
                    period,
                    parameterCd)

        # Rudimentary error handling - must be a more efficient way to do this?
        # AC - assert - need to study this more
        try:
            pd.read_json(testURL)['declaredType']['queryInfo']\
            == 'org.cuahsi.waterml.TimeSeriesResponseType'
            urlValid = True

        except ValueError as err:
            urlValid = False
            print("Value error: {0}.".format(err))
            print("The requested URL is invalid. Please check your input arguments.")
            
#         except HTTPError as err:
#             urlValid = False
#             print("HTTP error: {0}.".format(err))
#             print("The requested URL is invalid. Please check your imput arguments.")

        urlState = (fullURL, urlValid)
        return urlState
    
    def __getNWIS(self): 
        """
        Requests site information from USGS waterservices 
        when given a valid url following the REST protocol
        at https://waterservices.usgs.gov/rest/IV-Test-Tool.html

        The function waterServicesURL() should be used to develop 
        a valid REST url to waterservices.usgs. That function tests
        the url before passing it to this function for generation 
        of a dataframe object from the response file provided by 
        USGS.

        Returns:
        DataFrame of the requested site information.
        """
        print("Retrieving data.")
        
        url = self.__nwis_url
        
        # pcodes from usgs @
        # https://help.waterdata.usgs.gov/code/parameter_cd_query?fmt=rdb&inline=true&group_cd=%
        nwis_pcodes = {
            '00060': 'flow_cfs',
            '00065': 'stage',
            '00300': 'do_mass',
            '00010': 'wtemp_c',
            '00011': 'wtemp_f',
            '00095': 'spc_25',
            '00400': 'pH',
            '63680': 'turbidity_fnu'
        }
        
        # load file to local memory as json string
        ## ISSUE - use Requests not pd.read_json
        response = pd.read_json(url)

        # load top level keys with pertinent data
        responseType = response['declaredType']['timeSeries']
        value = response['value']

        # name T2 keys and get response info for QC
        vInfo = value['queryInfo']
        vSeries = value['timeSeries'] # a list of dicts for each param returned

        if len(vSeries) > 0:
        # the response contains at least one time series
            # response details
            responseURL = vInfo['queryURL']
            responseLoc = vInfo['criteria']['locationParam']
            responseVars = vInfo['criteria']['variableParam']
            responseSite = vSeries[0]['sourceInfo']['siteName']
            site = dict(
            {
                'siteID': responseLoc,
                'siteVariables': responseVars,
                'siteName': responseSite
            }   
            )
            
            self.siteinfo = site
            
            # check for a valid response type
            try: 
                k = list(response.keys())
                if k[1] == 'declaredType':
                    j = response.get(k[1])
                    if j['queryInfo'] ==\
                    'org.cuahsi.waterml.TimeSeriesResponseType':
                        True
                    else:
                        raise()
            except:
                print('Returned JSON is not of the correct type.')
                print('Please use the waterServicesURL() function to generate a valid URL.')

            # confirm the response is from the requested site
            try:
                if self.__nwis_site in site['siteID']:
                    True
                else:
                    raise()
            except:
                print('The USGS site is different than requested.')

            print('Loaded data from {}'.format(responseSite))

            # time zone details
            tzInfo = vSeries[0]['sourceInfo']['timeZoneInfo']
            tzDefault = tzInfo['defaultTimeZone']['zoneAbbreviation']
            tzDefaultOffset = tzInfo['defaultTimeZone']['zoneOffset']
            tzDS = tzInfo['daylightSavingsTimeZone']['zoneAbbreviation']
            tzDSOffset = tzInfo['daylightSavingsTimeZone']['zoneOffset']
            tz = dict(
            {
                'default': tzDefault,
                'defaultOffset': tzDefaultOffset,
                'daylightSavings': tzDS,
                'daylightSavingsOffset': tzDSOffset
            }
            )
            self.timezone = tz
            
            # geographic details
            geog = vSeries[0]['sourceInfo']['geoLocation']['geogLocation']
            geogDatum = geog['srs']
            lat = geog['latitude']
            lon = geog['longitude']
            
            if self.__elevation is None:
                navd88_ft = self.__elevationTNM(lon, lat)
            else:
                navd88_ft = self.__elevation
            navd88_m = navd88_ft*0.3048
            geoidHt_m, grs80_m = self.__grs80(lon, lat, navd88_m)
            geo = dict(
            {
                'datum': geogDatum,
                'latitude': lat,
                'longitude': lon,
                'navd88_ft': navd88_ft,
                'navd88_m': navd88_m,
                'geoidHt_m': geoidHt_m,
                'grs80_m': grs80_m
            }
            )
            self.geography = geo
            
            # Loop over parameter sets and place into Pandas series
            series = []
            for i in range(len(vSeries)):
                # variable (parameter) info
                var = vSeries[i]['variable']
                varCode = var['variableCode'][0]['value']
                varName = var['variableName']
                varUnit = var['unit']
                varND = var['noDataValue']

                if varCode in nwis_pcodes.keys():
                    colName = nwis_pcodes[varCode]
                else:
                    colName = varName

                # parameter time series
                values = vSeries[i]['values'][0]['value']

                # put into Pandas series
                s = pd.json_normalize(values)
                # check that values exist
                if 'dateTime' in s.columns:
                    # put into Pandas series
                    s['dateTime'] = pd.to_datetime(s['dateTime'],
                                                       yearfirst=True,
                                                       infer_datetime_format=True)
                    s = s.set_index('dateTime')
                    s.columns = [colName,'qc_{}'.format(colName)]
                    s.replace(to_replace = varND,
                              value = np.nan)
                    s[colName] = s[colName].astype(float)

                    # save to list for merge
                    series.append(s)
            # merge series into one DataFrame
            df = pd.concat(series,axis=1,sort=False)
            
            self.data = df
            
            # collect other relevant information into master dictionary
            dct = dict(
            {   
                'siteInfo': site,
                'timezone': tz,
                'geography': geo,
                'data': df
            })

            return dct
        else:
        # the response contains no timeseries
            print("The requested site ID ({}) does not have any instantaneous values available.".format(self.__nwis_site))
    
    def __getLocal(self):
        """
        Interfaces with the user's local hard drive or server to 
        retrieve the requested file, extract the pertinent information from the file, 
        transform it as necessary to construct a functional dictionary, and loads the 
        data to the dictionary. 
        
        Inputs:
        
        Returns:
            dct = dictionary of the same format as in `getNWIS`
                {
                    siteInfo: dict
                    timezone: dict
                    geography: dict
                    data: pd.DataFrame
                }
        References:
        
        Issues/Notes:
            1. Need to add a check on the horizontal datum and use API to 
               transform to NAD83(2011) if necessary. Or just require NAD83(2011), 
               but there are APIs for standard datum conversions. Just need to 
               constrain the acceptable datums.
               
            2. Testing on timezone and date formats needed.
        """
        
        filePath = self.__local_path
        sep = self.__sep
        columns = self.__local_cols
        units = self.__local_units
        site = self.siteinfo
        geog = self.geography
        time = self.timezone
        
        print("Reading file.")
        # Open the file and read into a DataFrame
        ## Requiring at present iteration that the file can be read by CSV
        df = pd.read_csv(filePath, delimiter=sep)
        df.columns = columns
        
        # assuming month-first timestamps
        df = df.set_index(pd.to_datetime(df['dateTime'],
                                       format=time['format'],
                                       exact=False,
                                       errors='raise')).drop('dateTime',axis=1)
        
        # make index tz-aware
        df.index = df.index.tz_localize(tz = time['tz'])
        
        # save data as instance attribute
        self.data = df
        
        # update geographic attributes
        ## ISSUE - CHECK HORIZONTAL DATUM AND TRANSFORM TO NAD83(2011) IF NEEDED
        
        datum = geog['datum']
        lon = geog['longitude']
        lat = geog['latitude']
        navd88_ft = geog['navd88_ft']
        navd88_m = geog['navd88_m']
        
        print("Building geographic dictionary.")
        # Check if elevation is known
        if navd88_ft is None:
            if navd88_m is None:
                navd88_ft = self.__elevationTNM(lon, lat)
                navd88_m = navd88_ft*0.3048
            else:
                navd88_ft = navd88_m/0.3048
        
        # get height above geoid and grs80 height above ellipsoid
        geoidHt_m, grs80_m = self.__grs80(lon, lat, navd88_m)
        geo = dict(
        {
            'datum': datum,
            'latitude': lat,
            'longitude': lon,
            'navd88_ft': navd88_ft,
            'navd88_m': navd88_m,
            'geoidHt_m': geoidHt_m,
            'grs80_m': grs80_m
        }
        )
        self.geography = geo
        
        # --- Must end with the same data structure as getNWIS() --- #
        dct = dict(
        {   
            'siteInfo': site,
            'timezone': time,
            'geography': geo,
            'data': df
        })
        print("File loaded.")
        return dct
        
    def __oxsat(self, wtemp):
        
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
        elev = self.srcDat['geography']['navd88_m']/1000
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
    
    def __setSolarObserver(self):
        
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
                
    def __solar(self, date):
        
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
        
        obs = self.__solarObserver
        time = Time(date, location=obs.location)
        sr_utc = obs.sun_rise_time(time,'next').iso
        sn_utc = obs.noon(time,'next').iso
        ss_utc = obs.sun_set_time(time,'next').iso
        return (sr_utc,sn_utc,ss_utc)
    
    def __adm(self):
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
        
        siteInfo = self.srcDat['siteInfo']
        timeZone = self.srcDat['timezone']
        geography = self.srcDat['geography']
        data = self.srcDat['data']
        solarObserver = self.__solarObserver
        
        # check for NaNs in wtemp and do_mass
        ## replace QC values with 'd2k_interp' if nan
        ### interpolate NaNs
        cols = [i for i in self.data.columns]
        if 'qc_wtemp_c' in cols:
            # for NWIS
            # if temperature reading is bad, so is dissox reading
            self.data.loc[self.data.wtemp_c.isna(), 'do_mass'] = np.nan
            # track where interpolation was performed in qc column
            self.data.qc_wtemp_c = self.data.qc_wtemp_c.fillna(value='d2k_interp')
            # perform interpolation on temperature
            self.data.wtemp_c = self.data.wtemp_c.interpolate(method='time')
            
        else:
            # for local files
            self.data.assign(qc_wtemp_c = 'P')
            self.data.loc[self.data.wtemp_c.isna(), 'qc_wtemp_c'] = 'd2k_interp'
            # if temperature reading is bad, so is dissox reading
            self.data.loc[self.data.wtemp_c.isna(), 'do_mass'] = np.nan
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
        self.data = self.data.assign(osat = self.__oxsat(self.data.wtemp_c))
#         osat = pd.Series(self.__oxsat(df.wtemp_c),name='osat')
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
                            pd.to_datetime(self.__solar(x)[0],
                                           utc=True).
                                   tz_convert(x.tz)))
        # solnoon
        dfdaily = dfdaily.assign(solnoon=
            dfdaily.index.to_series().
                  apply(lambda x: 
                            pd.to_datetime(self.__solar(x)[1],
                                           utc=True).
                                   tz_convert(x.tz)))
        # sunset
        dfdaily = dfdaily.assign(sunset=
            dfdaily.index.to_series().
                  apply(lambda x: 
                            pd.to_datetime(self.__solar(x)[2],
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

    def __arrh(self,k20,T,theta):
        """
        Returns a temperature corrected rate coefficient using 
        the simplified Arrhenius equation

        Args:
        k20 =   rate at 20 celsius
        T =     temperature of interest
        theta = temperature coefficient for reaction of interest
        """
        return k20*theta**(T-20)

    def __photo(self,p,f,t,tsr,temp):
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

    def __derivs(self,t,c,temp_int,trise,f,est):

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
        dosat = self.__oxsat(temp_t)

        # unpack estimated values
        ka = est[0]
        p = est[1]
        r = est[2]

        # calculate rates at temp(t)
        ka_t = ka*1.024**(temp_t-20)
        r_t = r*1.07**(temp_t-20)

        # calculate photosynthesis at this time
        p_t = self.__photo(p,f,t,trise,temp_t)

        # calculate net rate for this time step
        dc = np.zeros(1)
    #     dc[0] = ka_t*(dosat-c[0])+p_t-r_t
        dc = ka_t*(dosat-c)+p_t-r_t
    #     dc = dc.reshape((1,))

        return dc

    def __residuals(self,est,temp_int,
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
                 self.__derivs(t,c,temp_int,trise,f,est),
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

    def __rpd(self,adm_est,fit_est):
        """
        Compute relative percent difference between initial and 
        fitted estimators.
        """
        avg = [(adm_est[i] + fit_est[i])/len(fit_est) for i in range(len(fit_est))]
        diff = fit_est - adm_est
        rd = diff/avg
        return rd

    def __fitDay(self, fitdate, user_est, print_results, method):
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

        # set optimization bounds for each parameter
        bounds = [(0,100),(0,None),(0,None)]
        
        # Minimize the sum of squared residuals between
        # observed and predicted dissolved oxygen concentrations
        # by adjusting the three-parameter estimate of [ka, maxP, meanR]
        # as provided by the ADM result for each day (or by the user as an array)
        
        if method == 'Nelder-Mead':
            opt = minimize(self.__residuals,est,
                                method='Nelder-Mead',
                                options={'xatol': 1e-6},
                                args=(temp_int,
                                    trise,f,tspan,y0,
                                    tdata,do_obs.values,
                                    today))
        if method == 'SLSQP':
            opt = minimize(self.__residuals,est,
                                method='SLSQP',
                                tol = 1e-6,
                                bounds=bounds,
                                options={'maxiter': 1000},
                                args=(temp_int,
                                    trise,f,tspan,y0,
                                    tdata,do_obs.values,
                                    today))
            
        if method == 'L-BFGS-B':
            opt = minimize(self.__residuals, est,
                           method = 'L-BFGS-B',
                           tol = 1e-6,
                           bounds = bounds,
                           args = (temp_int,
                                    trise,f,tspan,y0,
                                    tdata,do_obs.values,
                                    today))
            
        if method == 'Powell':
            opt = minimize(self.__residuals, est,
                           method = 'Powell',
                           tol = 1e-6,
                           bounds = bounds,
                           options = {'xtol': 1e-6, 'ftol': 1e-6},
                           args = (temp_int,
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
                 self.__derivs(t,c,temp_int,trise,f,fitEst),
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
        rpd_est = self.__rpd(est, fitEst)
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
                     #'fitD': fitD,
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
    
    def fit2DO(self, user_est=None, print_results=False, method='Powell'):
        """
        Performs a non-linear regression to optimize the fit of the three 
        metabolic parameters. Returns the fitted results as a dictionary for each 
        day in the `admResult` dataframe, accessible as `instance_name.admResult.fitResult`.
        
        Inputs:
            user_est: default is None, and the estimates resulting from the ADM approximation are used as initial guesses.
                      May be modified for single-day datasets by providing a list of numbers in the order: 
                      [ka, pMax, Rmean].
            
            print_results: prints a daily summary of optimization performance and results to the screen as text.
            
            method: the optimization algorithm to use. Default is a bounds-constrained Powell method. All options are set to a x-tolerance of 1e-6 for acceptable convergence. Bounds are fixed, and all parameters must be >= 0, while only reaeration is constrained from the right such that (ka <= 100). 
            Other allowable options include:
                    'Nelder-Mead', 'SLSQP', 'L-BFGS-B' (See Scipy.optimize.minize docs for more detail)
            
        """
        # set initial conditions
        if 'fit_do_init' in self.admResult.columns:
            self.admResult['fit_do_init'] = self.srcDat['data']['do_mass'].values[0]
        else:
            self.admResult = self.admResult.assign(fit_do_init = self.srcDat['data']['do_mass'].values[0])

        # Update admResult with fitResult
        self.admResult = self.admResult\
        .assign(fitResult = self.admResult.index.to_series()\
                .apply(lambda x: self.__fitDay(x.date(),user_est,print_results,method)))
        print("Optimization completed.")
    
    def plotSrcDat(self):
        """
        Plots the source data for visualization.
        
        Inputs:
        
        Returns:
        
        References:
        
        Notes/Issues:
            1. Improve graphics.
        
        """
        import matplotlib.pyplot as plt
        
        siteInfo = self.srcDat['siteInfo']
        timeZone = self.srcDat['timezone']
        geography = self.srcDat['geography']
        data = self.srcDat['data']
        admResult = self.admResult
        
        columns = data.columns
        dataColumns = [i for i in columns if 'qc' not in str(i)]
        data = data[dataColumns]
        plt.plot(data)
        
    def plotFitted(self):
        self.plotADM(plotFitted=True)
        
    def plotADM(self, plotFitted=False):
        """
        Plots the ADM results for visualization.
        
        Inputs:
        
        Returns:
        
        References:
        
        Notes/Issues:
        
        """
        from bokeh.models.widgets import Panel, Tabs
        from bokeh.io import output_file, show
        from bokeh.plotting import figure
        
        siteInfo = self.srcDat['siteInfo']
        timeZone = self.srcDat['timezone']
        geography = self.srcDat['geography']
        df = self.data
        dfdelta = self.admResult
        
        siteName = siteInfo['siteName']
        output_file(siteName.replace(' ','_')+"_data_plots.html")
        
        df.index = df.index.tz_localize(tz=None)
        dfdelta.index = dfdelta.index.tz_localize(tz=None)

        # Plot water temperature of record
        if 'wtemp_c' in df.columns:
            
            # build source columns
            temp_source = ColumnDataSource(data = dict(
                # strip tz info to bypass Bokeh's tz naivety
                x = df.index,
                y = df.wtemp_c
            ))
            # build plots
            p1 = figure(x_axis_type='datetime',
                        plot_width=1500, plot_height=750,
                        title=siteName)
            p1.circle('x', 'y', source=temp_source,
                       size=3, line_color="red", fill_color="red", fill_alpha=0.5,
                       legend_label="Water Temp")
            p1.line('x', 'y', source=temp_source, 
                    line_width=2, line_color="red", line_alpha=0.5)
            p1.xaxis.axis_label = 'Time'
            p1.yaxis.axis_label = 'Water Temperature (C)'
            p1.add_tools(HoverTool(
                            tooltips=[
                                        ('Time',    '@x{%F %H:%M}'),
                                        ('Temp',   '@y')],
                            formatters={
                            '@x':'datetime',
                            '@y':'printf'},mode='mouse',
                        ))
        
        # Plot dissolved oxygen of record
        if 'do_mass' in df.columns:
            
            # build source columns
            do_source = ColumnDataSource(data = dict(
                x = df.index,
                y = df.do_mass
            ))
            
            p2 = figure(x_axis_type='datetime',
                        x_range=p1.x_range,
                        plot_width=1500, plot_height=750,
                        title=siteName)
            p2.diamond('x', 'y', source=do_source,
                       size=3, line_color="navy", fill_color="navy", fill_alpha=0.5,
                       legend_label="Observed Dissolved Oxygen (mg/L)")
            p2.line('x', 'y', source=do_source, 
                    line_width=2, line_color="navy", line_alpha=0.5)
            
            osat_source = ColumnDataSource(data = dict(
                x = df.index,
                y = df.osat
            ))
            p2.line('x','y',source=osat_source,
                    line_width=2, line_color="navy", line_alpha=0.5, line_dash='dashed', legend_label="Oxygen Saturation")
            
        # Plot pH of record
        if 'pH' in df.columns:
            
            ph_source = ColumnDataSource(data = dict(
                x = df.index,
                y = df.pH
            ))
            p2.circle_cross('x','y',source=ph_source,
                      legend_label="Observed pH",
                      size=2, 
                      line_color="purple", fill_color="purple", fill_alpha=0.5)
            p2.line('x','y',source=ph_source,
                    line_width=2, line_color="purple", line_alpha=0.5)
            p2.xaxis.axis_label = 'Time'
            p2.yaxis.axis_label = 'Dissolved Oxygen (mg/L)'
            p2.add_tools(HoverTool(
                            tooltips=[
                                        ('Time',    '@x{%F %H:%M}'),
                                        ('Value',   '@y')],
                            formatters={
                            '@x':'datetime',
                            '@y':'printf'},mode='mouse',
                        ))

        # Create figure for reaeration, meanP and meanR
        p3 = figure(x_axis_type='datetime',
                    x_range=p2.x_range,
                    title=siteName,
                    plot_width=1500, plot_height=750)
        
        # Build column data sources
        ka_source = ColumnDataSource(data = dict(
            x = dfdelta.index,
            y = dfdelta.ka
        ))
        mp_source = ColumnDataSource(data = dict(
            x = dfdelta.index,
            y = dfdelta.meanP
        ))
        mr_source = ColumnDataSource(data = dict(
            x = dfdelta.index,
            y = dfdelta.meanR
        ))
        
        p3.diamond('x', 'y', source=ka_source, 
                   legend_label="ADM Reaeration",
                   size=10, line_color="blue", fill_color="blue", fill_alpha=0.5)
        p3.circle('x','y', source=mp_source,
                 legend_label="ADM Productivity",
                 size=10, line_color="green", fill_color="green", fill_alpha=0.5)
        p3.circle('x','y', source=mr_source,
                  legend_label="ADM Respiration",
                  size=10, line_color="orange", fill_color="orange", fill_alpha=0.5)
        
        if 'pH' in df.columns:
            
            ph_source = ColumnDataSource(data = dict(
                x = df.index,
                y = df.pH
            ))
            p3.circle_cross('x','y',source=ph_source,
                      legend_label="Observed pH",
                      size=2, 
                      line_color="purple", fill_color="purple", fill_alpha=0.5)
            p3.line('x','y',source=ph_source,
                    line_width=2, line_color="purple", line_alpha=0.5)
        p3.add_tools(HoverTool(
                        tooltips=[
                                    ('Date',    '@x{%F %H:%M}'),
                                    ('Value',   '@y')],
                        formatters={
                        '@x':'datetime',
                        '@y':'printf'},mode='mouse',
                    ))
        p3.xaxis.axis_label = 'Time'
        p3.yaxis.axis_label = 'Value'   
        
        tab1 = Panel(child=p1, title='Water Temperature (Celsius)')
        tab2 = Panel(child=p2, title='Dissolved Oxygen (mg/L)')
        tab3 = Panel(child=p3, title='Reaeration, Productivity and Respiration')
        tabs = [tab1, tab2, tab3]
        if plotFitted == True:
            # plot fitted values as well
            p3.cross(dfdelta.index, dfdelta.fitResult.apply(lambda x: x['fit_ka']), 
                       legend_label="Fitted Mean Reaeration",
                       size=14, line_color="blue", fill_color="blue", fill_alpha=0.0),
            p3.circle_cross(dfdelta.index, dfdelta.fitResult.apply(lambda x: x['fit_maxP']), 
                     legend_label="Fitted Max Productivity",
                      size=14, line_color="green",fill_color="green", fill_alpha=0.0),
            p3.circle(dfdelta.index, dfdelta.fitResult.apply(lambda x: x['fit_meanP']), 
                     legend_label="Fitted Mean Productivity",
                     size=14, line_color="green", fill_color="green", fill_alpha=0.0)
            p3.circle(dfdelta.index, dfdelta.fitResult.apply(lambda x: x['fit_meanR']), 
                      legend_label="Fitted Respiration",
                      size=14, line_color="orange", fill_color="orange", fill_alpha=0.0)
        
            # make new tab for comparison of prediction
                    # Plot dissolved oxygen of record
            if 'do_mass' in df.columns:
                p4 = figure(x_axis_type='datetime',
                            x_range=p1.x_range,
                            title=siteName,
                           plot_width=1500, plot_height=750)
                p4.diamond(df.index, df.do_mass, 
                           size=3, line_color="red", fill_color="red", fill_alpha=0.5,
                           legend_label="Observed Dissolved Oxygen (mg/L)")
                p4.line(df.index, df.do_mass, 
                        line_width=2, line_color="red", line_alpha=0.5)
                
                # Plot predicted do
                do_pred = pd.concat([dfdelta.fitResult[i]['do_pred'] for i in range(len(dfdelta.fitResult))],axis=0)
                do_pred.index = do_pred.index.tz_localize(tz=None)
                err_index = dfdelta.index
                init_err = np.array([i['true_init_err'] for i in dfdelta.fitResult])
                
                p4.line(do_pred.index, do_pred.values, 
                        line_width=2, line_color="blue", line_alpha=0.5,
                        legend_label="Predicted Dissolved Oxygen (mg/L)")
                p4.cross(err_index, init_err,
                         line_width=2, line_color='red', line_alpha=0.5,
                         legend_label="Initial Condition Error (mg/L)")
                p4.line(err_index, np.zeros(len(err_index)),
                        line_width=1, line_color="red", line_alpha=0.8)
                p4.add_tools(HoverTool(
                    tooltips=[
                            ('Date',    '@x{%F %H:%M}'),
                            ('Value',   '@y')],
                    formatters={
                        '@x':'datetime',
                        '@y':'printf'},mode='mouse',
                    ))
                p4.xaxis.axis_label = 'Time'
                p4.yaxis.axis_label = 'DO (mg/L)'
            tab4 = Panel(child=p4, title='Predicted vs. Observed Dissolved Oxygen')
            tabs = [tab1, tab2, tab3, tab4]

        tabs = Tabs(tabs=tabs)

        show(tabs)