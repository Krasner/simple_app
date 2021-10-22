import os, sys
import argparse
from shutil import copyfile

from bokeh.plotting import curdoc
import panel as pn
pn.extension()

import re

def incrementString(x):
    m = re.search(r'\d+$', x)
    if m is None:
        return x+'1'
        
    return x[:m.span()[0]]+str(int(m.group())+1)

class mainPage():
    def __init__(self, host="https://localhost:5006/", app_name="app", **kwargs):
        self.host = host
        self.app_name = app_name
        
        self.image_choices = dict(
            none='',
            cat='./static/cat.jpg',
            dog='./static/dog.jpg',
            tree='./static/tree.jpg',
        )

        self.save_folder = './save'

        self.screen = self.do_layout()

    def search_callback(self,event):
        query = self.select.value
        if query == 'none':
            self.screen[1] = pn.Spacer(height=500)
        else:
            self.screen[1] = pn.pane.JPG(self.image_choices[query],height=500,embed=True)

    def save_callback(self,event):
        if self.select.value == 'none':
            return
        obj = self.screen[1].object
        filename = obj.split('/')[-1].split('.')[0]
        while os.path.exists(os.path.join(self.save_folder,filename+'.jpg')):
            filename = incrementString(filename)
        copyfile(obj,os.path.join(self.save_folder,filename+'.jpg'))

    def do_layout(self):
        self.select = pn.widgets.Select(name='Image Select',options = list(self.image_choices.keys()) )
        self.select.param.watch(self.search_callback, 'value')

        self.image_display = pn.Spacer(height=500)
        self.save_button = pn.widgets.Button(name='Save', button_type='primary')
        self.save_button.on_click(self.save_callback)
        return pn.Column( self.select, self.image_display, self.save_button)

if __name__ == "__main__":
    # input arguments:
    #parser = argparse.ArgumentParser()


    app = mainPage(host=''.join(["http://","localhost",":5006"]),app_name="simple_app")
    
    srvr = pn.io.server.get_server({'simple_app': app.screen},port=5006, static_dirs={'simple_app/static': './static'}, num_procs=1)
    srvr.start()
    srvr.io_loop.start()
