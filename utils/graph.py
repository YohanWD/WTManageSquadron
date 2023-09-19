from db_functions import db_funct
import matplotlib.pyplot as plt
from datetime import datetime

# Function to generate activity graph base on the members activity
def generate_activity_graph(db_name,path_to_save_graph):
    for el in db_funct.get_all_squad_members(db_name):
        history_list = db_funct.get_activity_history_from_members(db_name, el.id)
        x_list = []
        y_list = []
        for elem1, elem2 in history_list:
            tmptime = datetime.strptime(elem2, '%Y-%m-%d %H:%M:%S')
            x_list.append(datetime.strptime(tmptime.strftime('%Y-%m-%d'),'%Y-%m-%d'))
            y_list.append(elem1)
            
        plt.clf()
        plt.xlabel('x - time')
        plt.ylabel('y - activity')
        plt.ylim(0, 4000)
        for i in range(len(x_list)):
            plt.annotate(y_list[i], xy=(i, y_list[i]),xytext=(-12.5,7), textcoords='offset points')
        plt.gcf().autofmt_xdate()
        plt.plot_date(x_list,y_list,color='green', linestyle='-', linewidth = 2,
            markerfacecolor='blue', markersize=7,xdate=True)
        plt.title(f'Activity history of {el.pseudo}')
        plt.savefig(f'{path_to_save_graph}/{el.pseudo}.png')