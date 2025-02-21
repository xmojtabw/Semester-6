int f(int n)
{
    int r = 0;
    for(int i=2 ; i<=n; i = pow(i,2))
    {
        r++; 
    }
    return r ;
}

int f(int n , int m)
{
    long long r = 0 ; 
    for (int i =2 ; i<n ; i*=3)
    {
        for (int j =0 ; j<m;j+=2)
        {
            for(int k =0 ; k<j ; k++)
            {
                r +=1;
            }
        }
    }
    return r ;
}

int f(int r )
{
    if (r<=1) return r ; 
    return f(r-2) + f(r-1);
}

int f(n)
{
    if (n<=1)
    {
        f(n-2);
        int r = 2 * f(n-1) + n;
        return r;
    }
}

// int f(n){
//     int r = 0 ;  
//     for i = 1 to n do: 
//         for j=1 to i do :
//             for k=j to i+j do :
//                 r=r+1
    
// return(r)
// }