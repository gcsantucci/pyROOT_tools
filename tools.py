import ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, TTree, gRandom, TH1F, TH2F, TLegend, TLine

#############################################################################################     
# Get the number of entries in a tree after some cut:
def GetEntries(tree, cut):
    return int(tree.Draw("",cut))

#############################################################################################  
# Whether or not to draw the statiscs box
def DrawBox(h,x1,x2,y1,y2):
    st = (h.FindObject("stats"))
    st.SetX1NDC(x1)
    st.SetX2NDC(x2)
    st.SetY1NDC(y1)
    st.SetY2NDC(y2)
    st.SetOptStat(111);

#############################################################################################            
# Set Stats Box:                                                        
def SetStatsBox(stats):
    ROOT.gStyle.SetOptStat("emr")
    ROOT.gStyle.SetStatX(0.92);    # Top right corner.           
    ROOT.gStyle.SetStatY(0.92)
    if not stats:
        ROOT.gStyle.SetOptStat(0)

#############################################################################################      
# Get Legend Box:           
def GetLegend(h1, names, title=None):
    leg = TLegend(.7,.62,.9,.82)
    if title:
        leg.SetHeader(title)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)
    for h, name in zip(h1, names):
        leg.AddEntry(h, name, 'L')
    return leg

################################################################################## 
# Get a TLine:
def GetLine(l):
    x1,y1,x2,y2 = l
    return TLine(x1,y1,x2,y2)

#############################################################################################        
# Save a figure
def Save(c1, path, name):
    for extension in ['.png', '.jpg', '.C']:
        c1.Print(path + name + extension)

#############################################################################################  
# Declare a Histogram:
def Hist(name='h', nbins=100, xmin=0, xmax=100, title='', xlabel='', ylabel=''):
    return TH1F(name,'{0};{1};{2}'.format(title, xlabel, ylabel), nbins, xmin, xmax)

############################################################################################# 
# Declare a 2D Histogram:        
def Hist2D(name='h', nbins=100, xmin=0, xmax=100,
           nbins2=100, xmin2=100, xmax2=200, 
           title='', xlabel='', ylabel=''):
    return TH2F(name,'{0};{1};{2}'.format(title, xlabel, ylabel), nbins, xmin, xmax, nbins2, xmin2, xmax2)

#############################################################################################  
# Draw a variable from a tree:
def Draw(c1, tree, var='', cut='', option='', log=False):
    total = tree.Draw(var,cut, option)
    if log:
        c1.SetLogy(1)
    c1.Draw()
    c1.SetLogy(0)
    return float(total)

#############################################################################################  
# Draw a histogram of a variable from a tree:
def DrawHist(c1, tree, var='', cut='', option='',
             nbins=100, xmin=0, xmax=100,
             title='', xlabel='', ylabel='', col=1, log=False, norm=False,
             stats=True, leg=False, save=False):
    SetStatsBox(stats)
    h1 = Hist('h1', nbins, xmin, xmax, title, xlabel, ylabel)
    h1.SetLineColor(col)
    h1.SetLineWidth(2)
    tree.Draw('{}>>h1'.format(var), cut, option)
    if log:
        c1.SetLogy(1)
    if norm:
        h1.Scale(1/h1.Integral())
        h1.Draw()
    if leg:
        leg = GetLegend([h1], leg)
        leg.Draw()
    c1.Draw()
    if save:
        c1.SaveAs(save)
    c1.SetLogy(0)
    del h1
    return c1

#############################################################################################    
# Draw a 2D histogram of a variable from a tree:                                    
def DrawHist2D(c1, tree, var='', cut='', option='',
               nbins=100, xmin=0, xmax=100,
               nbins2=100, xmin2=0, xmax2=100,
               title='', xlabel='', ylabel='', col=1, log=False):

    h1 = Hist2D('h1', nbins, xmin, xmax,
                nbins2, xmin2, xmax2,
                title, xlabel, ylabel)
    h1.SetMarkerColor(col)
    tree.Draw('{}>>h1'.format(var), cut, option)
    if log:
        c1.SetLogy(1)
    c1.Draw()
    c1.SetLogy(0)
    del h1
    return c1

#############################################################################################
# Draw two histograms from two trees:
def Draw2Hists(c1, tree1, tree2, var='', var2=None, cut1='', cut2='', 
               nbins=100, xmin=0, xmax=100,
               title='', xlabel='', ylabel='',
               col1=2, col2=4, log=False, norm=False, save=False, show=True,
               stats=True, leg=None, line=None):
    SetStatsBox(stats)
    if not var2:
        var2 = var
    h1 = Hist('h1', nbins, xmin, xmax, title, xlabel, ylabel)
    h2 = Hist('h2', nbins, xmin, xmax)
    h1.SetLineColor(col1)
    h1.SetLineWidth(2)
    h2.SetLineColor(col2)
    h2.SetLineWidth(2)
    tree1.Draw("{}>>h1".format(var), cut1)
    tree2.Draw("{}>>h2".format(var2), cut2,"same")
    if norm:
        h1.Scale(1/h1.Integral())
        h2.Scale(1/h2.Integral())
        h1.Draw()
        h2.Draw('SAMES')
    if leg:
        leg = GetLegend([h1, h2], leg)
        leg.Draw()
    if line:
        lines = [GetLine(l) for l in line]
        for l in lines:
            l.Draw()
    if log:
        c1.SetLogy(1)
    if show:
        c1.Draw()
    if save:
        c1.SaveAs(save)
    c1.SetLogy(0)
    del h1
    del h2
    return c1

##################################################################################
# Draw two 2D histograms from two trees:                
def Draw2Hists2D(c1, tree1, tree2, var='', var2=None,
                 cut1='', cut2='',
                 nbins=100, xmin=0, xmax=100,
                 nbins2=100, xmin2=0, xmax2=100,
                 title='', xlabel='', ylabel='',
                 col1=2, col2=4, log=False):

    if not var2:
        var2 = var

    h1 = Hist2D('h1', nbins, xmin, xmax,
                nbins2, xmin2, xmax2,
                title, xlabel, ylabel)
    h1.SetMarkerColor(col1)
    h2 = Hist2D('h2', nbins, xmin, xmax,
                nbins2, xmin2, xmax2,
                title, xlabel, ylabel)
    h2.SetMarkerColor(col2)
    tree1.Draw("{}>>h1".format(var), cut1)
    tree2.Draw("{}>>h2".format(var2), cut2,"same")

    if log:
        c1.SetLogy(1)
    c1.Draw()
    c1.SetLogy(0)
    del h1
    del h2
    return c1


##################################################################################   
# Read files to get the trees:
def GetTree(path='/Users/gabrielsantucci/Dropbox/PhD/SK/fiTQun_analysis/Knu_muGamma/atmnu/multiring/files/', f1='pdk/pdk_100k.root', f2=None, tree1='h1', tree2='treePDK'):
    tree = ROOT.TChain(tree1)
    tree.Add(path + f1)
    if f2:
        tree.AddFriend(tree2, path+f2)
    return tree

################################################################################## 

if __name__ == "__main__":
    pass
