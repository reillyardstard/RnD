
# coding: utf-8

# # Embedding Matplotlib Animations in IPython Notebooks

# *This notebook first appeared as a*
# [*blog post*](http://jakevdp.github.io/blog/2013/05/12/embedding-matplotlib-animations/)
# *on*
# [*Pythonic Perambulations*](http://jakevdp.github.io).
# 
# *License:* [*BSD*](http://opensource.org/licenses/BSD-3-Clause)
# *(C) 2013, Jake Vanderplas.*
# *Feel free to use, distribute, and modify with the above attribution.*

# <!-- PELICAN_BEGIN_SUMMARY -->
# I've spent a lot of time on this blog working with matplotlib animations
# (see the basic tutorial
# [here](http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/),
# as well as my examples of animating
# [a quantum system](http://jakevdp.github.io/blog/2012/09/05/quantum-python/),
# [an optical illusion](http://jakevdp.github.io/blog/2012/09/26/optical-illusions-in-matplotlib/),
# [the Lorenz system in 3D](http://jakevdp.github.io/blog/2013/02/16/animating-the-lorentz-system-in-3d/),
# and [recreating Super Mario](http://jakevdp.github.io/blog/2013/01/13/hacking-super-mario-bros-with-python/)).
# Up until now, I've not have not combined the animations with IPython notebooks.
# The problem is that so far the integration of IPython with matplotlib is
# entirely static, while animations are by their nature dynamic.  There are some
# efforts in the IPython and matplotlib development communities to remedy this,
# but it's still not an ideal setup.
# 
# I had an idea the other day about how one might get around this limitation
# in the case of animations.  By creating a function which saves an animation
# and embeds the binary data into an HTML string, you can fairly easily create
# automatically-embedded animations within a notebook.
# <!-- PELICAN_END_SUMMARY -->

# ## The Animation Display Function

# As usual, we'll start by enabling the pylab inline mode to make the
# notebook play well with matplotlib.

# In[1]:

get_ipython().magic(u'pylab inline')


# Now we'll create a function that will save an animation and embed it in
# an html string.  Note that this will require ffmpeg or mencoder to be
# installed on your system.  For reasons entirely beyond my limited understanding
# of video encoding details, this also requires using the libx264 encoding
# for the resulting mp4 to be properly embedded into HTML5. 

# In[3]:

from tempfile import NamedTemporaryFile

VIDEO_TAG = """<video controls>
 <source src="data:video/x-m4v;base64,{0}" type="video/mp4">
 Your browser does not support the video tag.
</video>"""

def anim_to_html(anim):
    if not hasattr(anim, '_encoded_video'):
        with NamedTemporaryFile(suffix='.mp4') as f:
            anim.save(f.name, fps=20, extra_args=['-vcodec', 'libx264'])
            video = open(f.name, "rb").read()
        anim._encoded_video = video.encode("base64")
    
    return VIDEO_TAG.format(anim._encoded_video)


# With this HTML function in place, we can use IPython's HTML display tools
# to create a function which will show the video inline:

# In[4]:

from IPython.display import HTML

def display_animation(anim):
    plt.close(anim._fig)
    return HTML(anim_to_html(anim))


# ## Example of Embedding an Animation

# The result looks something like this -- we'll use a basic animation example
# taken from my earlier
# [Matplotlib Animation Tutorial](http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/) post:

# In[5]:

from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=20, blit=True)

# call our new function to display the animation
display_animation(anim)


# ## Making the Embedding Automatic

# We can go a step further and use IPython's display hooks to automatically
# represent animation objects with the correct HTML.  We'll simply set the
# ``_repr_html_`` member of the animation base class to our HTML converter
# function:

# In[6]:

animation.Animation._repr_html_ = anim_to_html


# Now simply creating an animation will lead to it being automatically embedded
# in the notebook, without any further function calls:

# In[8]:

animation.FuncAnimation(fig, animate, init_func=init,
                        frames=100, interval=20, blit=True)


# So simple!  I hope you'll find this little hack useful!

# *This post was created entirely in IPython notebook.  Download the raw notebook*
# [*here*](http://jakevdp.github.io/downloads/notebooks/AnimationEmbedding.ipynb), *or see a static view on*
# [*nbviewer*](http://nbviewer.ipython.org/url/jakevdp.github.io/downloads/notebooks/AnimationEmbedding.ipynb).
