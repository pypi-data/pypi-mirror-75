# Python to LaTeX 

This is a module provides several method to parse data from Python to LaTeX.

Author:

* Sonja Stuedli

## Installation
`pip install --upgrade python_to_latex`

## Usage examples:
Below there are some small examples how to use the provided functions. Detailed explanation of each function can be found by using 

      import python_to_latex as p2l
      help(p2l.<function_name>)
      
### Printing a matrix:

  ```python
        import python_to_latex as p2l
        import numpy as np
        mat2lat(np.eye(2),matrix_style='bmatrix')
  ```
  This will print the code block below and return the string to produce it.
    
  ```latex
     \begin{bmatrix}
       1 &   0\\ 
       0 &   1\\ 
     \end{bmatrix}
  ```

### Printing table output:

   ```python
        import python_to_latex as p2l
        numeric_list_to_tabularx([[1,2,3],[4,5,6]],heading=['A','B','c'])
   ```

    The above code will print the code block below and return the string to produce it.

  ```latex
        \begin{tabularx}{\linewidth}{S[table-auto-round,table-omit-exponent,fixed-exponent=0]S[table-auto-round,table-omit-exponent,fixed-exponent=0]S[table-auto-round,table-omit-exponent,fixed-exponent=0]} \toprule
        {A} & {B} & {C}\\ \midrule
        1 & 2 & 3\\
        4 & 5 & 6\\\bottomrule 
        \end{tabularx}
  ```

### Saving a matplotlib figure:


   ```python
        import python_to_latex as p2l
        import numpy as np
        import matplotlib
        import matplotlib.pyplot as plt
        
        x = np.arange(15)
        y1 = 2*x
        y2 = x+5
        y3 = x
    
        fig1,plt1 = plt.subplots(nrows=1,ncols=2)
        plt1[0].plot(x,y1)
        plt1[0].plot(x,y2,'.',label="line a")
        plt1[1].plot(x,y3,label="line 1")
        plt1[0].set_ylabel('$\lambda_2$')
        plt1[1].set_xlabel('$b$')
        plt1[1].set_ylabel('$\lambda_N$')
        plt1[1].set_xlabel('$N$')
        plt1[0].legend(loc=1)
        plt1[0].set_label("test")
        fig1.show()
    
        fig2pgf(fig1,"test",retain_color=True,retain_linestyle=True)
   ```

The code above generates a simgle matplotlib figure and then saves that figure in PGF format in a file called test.tikz. The saved file can be loaded in LaTex.