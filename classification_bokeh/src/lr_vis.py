import numpy as np
import sklearn
import pandas as pd
from sklearn import datasets
from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, LinearColorMapper
from bokeh.plotting import figure, output_file, save
import bokeh.palettes as bp


class lr_vis():
    def __init__(self,N=100):
        self.N=N

    def run(self):
        self._load_iris()
        self._setup_plot()
        self._plot_contour()
        self._plot_circle()
        self._on_change()
        self._curdoc()

    def _load_iris(self):
        iris = datasets.load_iris()
        self.X = iris.data[:,:2]
        self.x1, self.x2 = self.X[:,0], self.X[:,1]
        self.label = iris.target
    
    def _setup_plot(self):
        self.plot = figure(plot_height=400, plot_width=400, 
                           title="Logistic Regression (elasticnet)",
                           tools="crosshair,pan,reset,save,wheel_zoom",
                           x_range=[self.x1.min(),self.x1.max()], 
                           y_range=[self.x2.min(),self.x2.max()])

        self.text = TextInput(title="title", value='Logistic Regression (elasticnet)')
        self.slide_dict={
            "C":Slider(title="C", value=1.0, start=1.0, end=10.0, step=0.1),
            "l1_ratio":Slider(title="l1_ratio", value=0.5, start=0.1, end=0.9, step=0.1)
        }
    
    def _plot_contour(self):
        model = linear_model.LogisticRegression(max_iter=10000,solver="saga",penalty="elasticnet",l1_ratio=0.5)
        model.fit(self.X,self.label)

        x1_mesh, x2_mesh = np.meshgrid(np.linspace(self.x1.min(), self.x1.max(), self.N),
                                       np.linspace(self.x2.min(), self.x2.max(), self.N))
        z = model.predict(np.array([x1_mesh.ravel(), x2_mesh.ravel()]).T)
        z = z.reshape(x1_mesh.shape)
        self.source_cont = ColumnDataSource(data=dict(z=[z]))
        self.plot.image(image="z", x=self.x1.min(), y=self.x2.min(), 
                        dw=self.x1.max()-self.x1.min(), dh=self.x2.max()-self.x2.min(), 
                        palette='Category10_3',global_alpha=0.4,source=self.source_cont)

    def _plot_circle(self):
        color_dict={k: v for (k, v) in zip([0,1,2],bp.all_palettes["Category10"][3])}
        colors = [color_dict[i] for i in self.label]
        source = ColumnDataSource(data=dict(x1=self.x1, x2=self.x2, colors=colors))
        self.plot.circle('x1', 'x2', source=source, size=5,color="colors")

    def _update_title(self,attrname, old, new):
        self.plot.title.text = self.text.value
    
    def _update_data(self,attrname, old, new):
        param_dict={}
        for key,val in self.slide_dict.items():
            param_dict[key]=val.value

        model = linear_model.LogisticRegression(max_iter=10000,solver="saga",penalty="elasticnet",**param_dict)
        model.fit(self.X,self.label)
        x1_mesh, x2_mesh = np.meshgrid(np.linspace(self.x1.min(), self.x1.max(), self.N),
                                       np.linspace(self.x2.min(), self.x2.max(), self.N))
        z = model.predict(np.array([x1_mesh.ravel(), x2_mesh.ravel()]).T)
        z = z.reshape(x1_mesh.shape)

        self.source_cont.data = dict(z=[z])

    def _on_change(self):
        self.text.on_change('value', self._update_title)
        for w in self.slide_dict.values():
            w.on_change('value', self._update_data)

    def _curdoc(self):
        inputs = column(self.text, *self.slide_dict.values())
        curdoc().add_root(row(inputs, self.plot, width=800))
        curdoc().title = "Sliders"


lrvis=lr_vis()
lrvis.run()





