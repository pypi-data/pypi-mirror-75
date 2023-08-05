import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import OLSResults
        
def tidy(self, conf_int=None, conf_level=.05):
        """Create table of regression coefficients

        Parameters
        -----------
        self : an OLSResults object
        conf_int : string, optional
            create confidence intervals
        conf_level : float
            confidence level for the confidence intervals

        Returns
        -------
        The table of coefficients as a Pandas DataFrame

        See Also
        --------
        glance

        """
        
        tdf = pd.DataFrame({'coefs':self.params, 
                            'stderr':self.bse, 
                            'tvalues':self.tvalues, 
                            'pvalues':self.pvalues},
                        index = self.model.exog_names)
        return tdf



def glance(self):
        """Create table of ancillary regression statistics

        Parameters
        -----------
        self : an OLSResults object
        
        Returns
        -------
        The table of statistics as a Pandas DataFrame

        See Also
        --------
        tidy

        """

        gdf = pd.DataFrame({'r_squared':self.rsquared,
                            'adj_r_squared':self.rsquared_adj,
                            'sigma':np.sqrt(self.ssr/self.df_resid),
                            'statistic':self.fvalue,
                            'p_value':self.f_pvalue,
                            'df':self.df_model+1,
                            'logLik':self.llf,
                            'aic':self.aic,
                            'bic':self.bic,
                            'deviance':self.ssr,
                            'df_residual':self.df_resid},
                       index=[0])

        return gdf
 
def sumary(self):
    """Brief linear model output
    
    Parameters
    -----------
    self : an OLSResults object
    
    Returns
    -------
    nothing
    
    
    See Also
    --------
    
    summary from statsmodels
    """
    
    tdf = tidy(self)

    print(tdf.to_string(formatters={'coefs':'{:,.3f}'.format,
                                    'stderr':'{:,.3f}'.format,
                                    'tvalues':'{:,.2f}'.format,
                                    'pvalues':'{:,.4f}'.format}))
    
    print("\nn={0:.0f} p={1:.0f} Residual SD={2:.3f} R-squared={3:.2f}".format(
        self.nobs, self.df_model+1, np.sqrt(self.ssr/self.df_resid), self.rsquared))

    if(self.eigenvals[-1] < 1e-10):
            print("Warning: Strong collinearity - design may be singular")
    
    return
          
         
        
OLSResults.tidy = tidy
OLSResults.glance = glance
OLSResults.sumary = sumary
