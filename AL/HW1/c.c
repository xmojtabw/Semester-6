int f(n)
{
    int r;
    if (n<=1)
    {
        r = n;
    }
    else
    {
       int r = 2 * f(n-1) + n;
    }
    return r;
}
