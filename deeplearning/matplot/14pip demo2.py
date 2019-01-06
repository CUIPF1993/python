import matplotlib.pyplot as plt

labels = 'Frogs','Hogs','Dogs','Logs'
fracs = [15,30,45,10]

ax1 = plt.subplot2grid((2,2),(0,0),rowspan=1,colspan=1)
ax2 = plt.subplot2grid((2,2),(0,1),rowspan=1,colspan=1)
ax3 = plt.subplot2grid((2,2),(1,0),rowspan=1,colspan=1)
ax4 = plt.subplot2grid((2,2),(1,1),rowspan=1,colspan=1)

ax1.pie(fracs,labels=labels,autopct='%1.1f%%',radius=1)
ax2.pie(fracs,labels=labels,autopct='%1.1f%%',radius=1)
ax3.pie(fracs,labels=labels,autopct='%1.1f%%',radius=0.5,textprops={'size':'smaller'})
ax4.pie(fracs,labels=labels,autopct='%1.1f%%',radius=0.5,textprops={'size':'smaller'})


plt.show()