This is a bird song generator by ilknuricke

https://github.com/ilknuricke/birdsong_generator_CPG

but in python!

To see how it works, see the original, especially this wonderfull blog http://mindwriting.org/blog/?p=229

Changes compared to the original:
 - Brain and syrinx models are merged into a single set of ODE to avoid the interpolation
 - Duration of a syllable is 0.3 s, not 0.24 s as stated in the original source

Variables meaning (see the original):  
y = [ xp , y , xk,  x , y  ]  
xp,y,xk - brain variables  
x,y - syrinx variables  

Some changes would have to be done to remove the pops between the syllables

