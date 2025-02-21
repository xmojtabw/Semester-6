f(n):
    r = 0 
    for i = 1 to n do: 
        for j=1 to i do :
            for k=j to i+j do :
                r=r+1
    
return(r)