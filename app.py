from motion_detector import df
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool,ColumnDataSource



# Optional perparing data for the hover_tool
df["Start_str"] = df['Start'].dt.strftime("%D %H:%M:%S")
df["End_str"] = df['End'].dt.strftime("%D %H:%M:%S")
# Optional perparing ColumnDataSource 
source = ColumnDataSource(df)


#1# prepare some data
# from dataFrame

#2# create figure object
f=figure(x_axis_label = "Time",x_axis_type = "datetime",height=300,title= "Motion Graph",sizing_mode='stretch_width')

#3# styling
f.title.text_color = "red"
f.title.text_font = "times"
f.title.text_font_style = "italic"
f.yaxis.minor_tick_line_color = None # to remove the scale line from yaxis


# Optional adding a hover tool 
hover = HoverTool(tooltips= [("Start", "@Start_str"),("End","@End_str")])
f.add_tools(hover)

#4# create a quad plot
#f.quad(left=df["Start"],right=df["End"],bottom=0,top=1,color="green")


# Start and End the column date names
f.quad(source = source, left="Start",right="End",bottom=0,top=1,color="green") # use this if u use ColumnarDataSource


#5# prepare the output_file
output_file('motion_graph.html')

#6# show the file 
show(f)

# Ref:https://docs.bokeh.org/en/latest/docs/reference/plotting.html