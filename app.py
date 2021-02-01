from motion_detector import df
from bokeh.io import output_file, show
from bokeh.plotting import figure



#1# prepare some data
# from dataFrame

#2# create figure object
f=figure(x_axis_label = "Time",x_axis_type = "datetime",height=300,title= "Motion Graph",sizing_mode='stretch_width')

#3# styling
f.title.text_color = "red"
f.title.text_font = "times"
f.title.text_font_style = "italic"


#4# create a quad plot
f.quad(left=df["Start"],right=df["End"],bottom=0,top=1,color="green")

#5# prepare the output_file
output_file('motion_graph.html')

#6# show the file 
show(f)

# Ref:https://docs.bokeh.org/en/latest/docs/reference/plotting.html