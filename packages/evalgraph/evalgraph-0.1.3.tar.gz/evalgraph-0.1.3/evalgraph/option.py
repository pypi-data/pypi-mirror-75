import datetime as dt, pandas as pd
from scipy.stats import norm
import math
from evalgraph.core.nodes import node, nodefn

class Market:
    def __repr__(self):
        return str(self.__class__.__name__)
    @node
    def PricingDate(self):
        return dt.datetime.now().date()

    @nodefn
    def MarketSpot(self,underlier):
        if underlier == 'SPY':
            return 300
        if underlier == 'SPX':
            return 3000
    
    @node
    def Volatility(self):
        return 0.2
 
class NodeObject:
    def __init__(self,**kwargs):
        for k,v in kwargs.items():
            getattr(self,k).set(v)

class Underlier(NodeObject):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    @node
    def Ticker(self):
        return 'SPX'
    
    @node
    def Spot(self):
        return Market().MarketSpot(self.Ticker())()

    @node
    def Volatility(self):
        return Market().Volatility()
    
class Option(NodeObject):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    @node
    def Underlier(self):
        return Underlier()
    
    @node
    def Description(self):
        type = {'C': 'Call', 'P': 'Put'}[self.OptionType()]
        return f"{type}[K={self.Strike()},Mat={self.Maturity().strftime('%Y/%-m/%-d')}]"   
    
    @node
    def Strike(self):
        return Market().MarketSpot(self.Underlier().Ticker())()
    
    @node
    def OptionType(self):
        return "C"
    
    @node
    def Price(self):
        sqrdt = self.Underlier().Volatility() * math.sqrt(self.Tenor())
        d1 = math.log(self.Underlier().Spot()/self.Strike())/sqrdt-0.5*sqrdt
        d2 = d1 - sqrdt
        return self.Underlier().Spot() * norm.cdf(d1) - self.Strike() * norm.cdf(d2)
    
    @node
    def PctPrice(self):
        return self.Price() / self.Underlier().Spot()
    
    @node
    def Delta(self):
        sqrdt = self.Underlier().Volatility() * math.sqrt(self.Tenor())
        d1 = math.log(self.Underlier().Spot()/self.Strike())/sqrdt-0.5*sqrdt
        return norm.cdf(d1)
    
    
    @node
    def Maturity(self):
        return Market().PricingDate() + pd.Timedelta('365d')
    
    @node
    def Tenor(self):
        return (self.Maturity() - Market().PricingDate()).days / 365.
    
    @nodefn
    def Test(self,x):
        return x * self.Strike()
   
if __name__ == "__main__":
    from evalgraph.core.graphevaluator import GraphEvaluator
    GraphEvaluator.verbose = False
    und = Underlier(Ticker='SPY')
    o = Option(OptionType='C',Underlier=und,Strike=und.Spot())
    #o.Price()
    #o.Price.deps
    print(o.Description())
    o.Price()
    #Market().PricingDate()