
import numpy as np
from .controller_abstracts import ControllerInterface

class MapController(ControllerInterface):

    click_range = 1/100

    def __init__(self,controller):
        super().__init__(controller)
        self.pressed  = False
        self.delete_gridline=False
        self.location    = None
        self.create_grid = False

    def _key_press_event(self,event):
        if event.key=='d':
            self.delete_gridline= not self.delete_gridline

        if event.key=='g':
            self.create_grid = not self.create_grid

        if event.key=='x' and not self.create_grid:
            xdata = event.xdata
            ydata = event.ydata
            location = (xdata,ydata)
            self.model.add_control_point('x',location)
        elif event.key=='x':
            self.model.add_grid_from_selection('x')

        if event.key=='y' and not self.create_grid:
            xdata = event.xdata
            ydata = event.ydata
            location = (xdata,ydata)
            self.model.add_control_point('y',location)
        elif event.key=='y':
            self.model.add_grid_from_selection('y')

        if event.key=='w':
            self.model.save_grid_data()

        if event.key=='r':
            self.model.load_grid_data()


        if event.key=='h':
            title = "Map Selection Functionality"
            functionality = {
                'select individual station': 'click',
                'select station group': 'click and drag',
                'add latitude gridline' : 'y',
                'add longitude gridline': 'x',
                'load grid data'        : 'r',
                'activate grid delete mode': 'd',
                'save grid data'        : 'w',
                'create grid from selection' : 'g'
            }
            self.create_help_menu_string(title, functionality)

        if event.key=='x' or event.key=='y' or event.key=='r':
            self.update_mesh()


    def _update(self):
        data = self.model.get_mapping_data()
        self.view.map(data)

    def _button_release_event(self, event):
        axes_label = self.view.get_axes_of_click(event)

        if axes_label == 'map' and self.pressed and not self.delete_gridline:

            lat, lon = event.ydata, event.xdata
            other_loc= np.asarray((lat, lon))
            norm = np.linalg.norm(self.location-other_loc)

            if norm > 0.2:
                extent = {'latitude':  [self.location[0],lat],
                          'longitude':[self.location[1],lon]
                          }
                self.model.create_selection_cycler(extent=extent)
                selection = self.model.get_selection()
                self.set_selection(selection)

            else:
                radius = self.get_radius()
                extent = {'latitude':  [lat-radius, lat+radius],
                          'longitude': [lon-radius, lon+radius]
                          }

            self.model.create_selection_cycler(extent=extent)
            selection = self.model.get_selection()
            self.set_selection(selection)
            self.location=None
            self.pressed=False

        if self.delete_gridline:
            print('deleting gridline')
            xdata = event.xdata
            ydata = event.ydata
            location = (xdata, ydata)
            self.model.delete_closest_gridline(location)
            self.update_mesh()


    def set_selection(self, selection):
        if selection is not None:
            self.view.update_selection(selection)

    def update_mesh(self):
        self.view.update_grid(*self.model.get_gridpoints())

    def get_radius(self):
        extent = self.view.get_extent()
        xlim = extent[0]
        ylim = extent[1]
        xrange = xlim[0] - xlim[1]
        yrange = ylim[0] - ylim[1]
        avg   = (abs(xrange) + abs(yrange))/2.0
        radius = avg * self.click_range
        return radius

    def _button_press_event(self, event):
        axes_label = self.view.get_axes_of_click(event)
        if axes_label == 'map':
            lat, lon = event.ydata, event.xdata
            self.pressed  = True
            self.location = np.asarray((lat,lon))




