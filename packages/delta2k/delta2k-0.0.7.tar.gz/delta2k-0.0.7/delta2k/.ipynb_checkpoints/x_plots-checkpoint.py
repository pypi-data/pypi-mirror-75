from bokeh.models.widgets import Panel, Tabs
from bokeh.models import HoverTool
from bokeh.io import output_file, show
from bokeh.plotting import figure, ColumnDataSource
import numpy as np
import pandas as pd

class plots():
    """
    Serves as an interface to collect user specifications from 
    [sourceDataVisualizationUI] and [resultsVisualizationUI] and 
    handle plotting requirements for such data visualization. 
    Public attributes include srcPlot to hold plots pertaining to 
    source data, and admPlot to hold plots pertaining to ADM results. 
    Also implements the Jupyter or Bokeh interfaces indicated in the 
    data display output entities. Methods include:
        plotSrcDat(): plots the source data for visualization
        plotADMresult(): plots the ADM results for visualization
    """
    
    from bokeh.models.widgets import Panel, Tabs
    from bokeh.io import output_file, show
    from bokeh.plotting import figure
    import numpy as np
    
    def __init__(self, admResult):
        """
        
        """
        self.siteInfo = admResult.siteInfo
        self.timeZone = admResult.timezone
        self.geography = admResult.geography
        self.data = admResult.data
        self.admResult = admResult.admResult
        self.dataPlot = self.plotSrcDat()
        self.resultPlot = self.plotADM()
    
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
        
        data = self.data
        columns = data.columns
        dataColumns = [i for i in columns if 'qc' not in str(i)]
        data = data[dataColumns]
        plt.plot(data)
        
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
        
        siteName = self.siteInfo['siteName']
#         siteName = siteName.replace(' ','_')
        output_file(siteName.replace(' ','_')+"_data_plots.html")
        
        df = self.data
        dfdelta = self.admResult
#         print(len(df.index))
#         print(len(dfdelta.index))
        df.index = df.index.tz_localize(tz=None)
        dfdelta.index = dfdelta.index.tz_localize(tz=None)
#         print(len(df.index))
#         print(len(dfdelta.index))
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
                    line_width=2, line_color="navy", line_alpha=0.5, line_dash='dashed')
            
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