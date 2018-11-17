from numpy import loadtxt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import csv
from matplotlib import gridspec
from scipy.optimize import curve_fit
class Amptel_Spectrum():
    def channel_energy_calibration(self, Directory=False, PdfPages=False, point_label = False):
        data = loadtxt(Directory+'Energy_channel_calibration/channel_energy_calibration_full_range.txt')
        x = data[:, 0]
        y = data[:, 1]
        x_offset = np.array([x[0]-60, x[1]-20, x[2]-50, x[3]-50, x[4]-50,x[5]-100])
        y_offset = np.array([y[0]+0.2, y[1]+1.2, y[2]+1.0, y[3]+1.0, y[4]+1.0,y[5]+ 1.7])
        
        plt.grid(True)
        # line fit
        line_fit, pcov = np.polyfit(x, y, 1, full=False, cov=True)
        fit_fn = np.poly1d(line_fit)
        line_fit_legend_entry = 'Line fit: ax+b\na=$%.5f\pm%.5f$\nb=$%.5f\pm%.5f$' % (line_fit[0], np.absolute(pcov[0][0]) ** 0.5, line_fit[1], np.absolute(pcov[1][1]) ** 0.5)
        line1, = plt.plot(np.arange(0, 1500), fit_fn(np.arange(0, 1500)), '-', color='darkgrey', label=line_fit_legend_entry)
        points1, = plt.plot(x, y, '.', color='black', label="Data")   
        for i, txt in enumerate(point_label):
            plt.text(x_offset[i], y_offset[i], txt, size=10)
        plt.legend()#handles=[points1, line1])
        ax = plt.gca()
        plt.xlim(0, 1600)
        plt.ylim(0, 70)
        plt.xlabel('Channel number')
        plt.ylabel('Energy / keV')
        plt.tight_layout()
        plt.savefig(Directory+"Energy_channel_calibration/channel_energy_calibration.png", bbox_inches='tight')
        PdfPages.savefig()
        
    def energy_spectrum(self, Directory=False, PdfPages=False,sources=False,real_time=False,color = False):
        # energy calib E=a*x + b, x is the channel number
        a = 0.04258
        b = 0.09599
        for i in np.arange(len(sources)):
            fig = plt.figure()
            ax = fig.add_subplot(111)
            data = loadtxt(Directory +"Source_spectra/"+sources[i]+"/"+sources[i]+"_spectrum_calibrated.txt")
            x1 = np.arange(0, len(data), 1)
            x_calib = a * x1 + b
            y1 = data
            y_rate = y1 / real_time[i] 
            y_norm = y1 / np.max(y1)
            am, = plt.step(x_calib, y_norm, where='mid', label=sources[i], linewidth=0.6, color=color[i], zorder=1.3)  # default farben 
            plt.bar(x_calib, y_norm, width=0.0425, linewidth=0.6, color=color[i], zorder=1.2, label='_nolegend_')
            ax = plt.gca()
            if sources[i] =="Am":
                plt.xlim(0, 70)
                ax.annotate(r'$Am\ {\gamma}_{2,0}$', xy=(60, 0.95), xytext=(-5, 5), ha='right', textcoords='offset points', fontsize=8)
            if sources[i] =="Fe":
                plt.xlim(0, 15)
                ax.annotate(r'${K}_{\alpha}^{Fe}$', xy=(7.1, 0.95), xytext=(-5, 5), ha='right', textcoords='offset points', fontsize=8)
                ax.annotate(r'${K}_{\beta}^{Fe}$', xy=(7.5, 0.15), xytext=(-5, 5), ha='right', textcoords='offset points', fontsize=8)
            if sources[i] =="Cd":
                plt.xlim(0, 60)
                ax.annotate(r'${K}_{\alpha}^{Cd}$', xy=(25.0, 0.95), xytext=(-5, 5), ha='right', textcoords='offset points', fontsize=8)
                ax.annotate(r'${K}_{\beta}^{Cd}$', xy=(28.0, 0.15), xytext=(-5, 5), ha='right', textcoords='offset points', fontsize=8)
            if sources[i] =="Background":
                point_label=[r'${K}_{\alpha}^{Fe}$',r'${K}_{\alpha}^{Ni}$',r'${K}_{\alpha}^{Cu}$', r'${K}_{\alpha}^{Zn}$',r'${K}_{\alpha}^{Ga}$', 
                             r'${L}_{\gamma}^{pb}$',r'${K}_{\alpha}^{Ag}$',r'${K}_{\alpha}^{ln}$', r'${K}_{\beta}^{Ag}$']
                y=[0.19,0.12,0.1,0.08,0.05,0.45,0.95,0.58,0.55]
                x=[8.2,9.1,10.2,11.0,11.5,17.2,24.5,25.8,27.5]
                for j, txt in enumerate(point_label):
                    ax.annotate(txt, xy=(x[j], y[j]), xytext=(-5, 5), ha='right', textcoords='offset points', fontsize=8)
                plt.xlim(0, 45)
            ax.set_ylim(bottom=0)
            plt.xlabel('Energy / keV')
            plt.ylabel('Counts (normalized)')
            #ax.set_xscale('log')
            #ax.set_yscale('log')
            ax.legend(loc='upper right')
            plt.tight_layout()
            plt.savefig(Directory+"Source_spectra/"+sources[i]+"/"+sources[i]+"_spectrum_calibrated.png", bbox_inches='tight')
            PdfPages.savefig()               
    def close(self):
        PdfPages.close()

if __name__ == '__main__':
    global PdfPages
    Directory = "Amptek_Si_PIN_Detector/"
    sources = ["Background","Cd","Am","Fe"]
    color=['#1f77b4','#d62728','#7f7f7f', '#7e0044',"magenta",'red','#33D1FF',"maroon","yellow",'lightblue','#006381','grey']
    point_label=[r'${K}_{\alpha}^{Fe}$',r'${K}_{\beta}^{Fe}$', r'${K}_{\alpha}^{Mo}$', r'${K}_{\alpha}^{Cd}$',r'${K}_{\beta}^{Cd}$', r'$Am\ {\gamma}_{2,0}$']
    real_time=[661.16,60.715000,2148.976000 , 1.011000,6272.115000]  # Number is accumulation time
    PdfPages = PdfPages('output_data/Amptel_Spectrum' + '.pdf')
    scan = Amptel_Spectrum()
    scan.channel_energy_calibration(PdfPages=PdfPages, Directory=Directory,point_label=point_label)
    scan.energy_spectrum(PdfPages=PdfPages, Directory=Directory, sources =sources,real_time =real_time,color=color)
    
    scan.close()
    