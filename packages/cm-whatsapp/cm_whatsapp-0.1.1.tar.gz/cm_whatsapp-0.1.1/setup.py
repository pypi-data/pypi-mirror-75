from setuptools import setup

setup(
    name='cm_whatsapp',
    version='0.1.1',    
    description='Whatsapp-auto-messaging through cm.com',
    url='https://github.com/nikhil130yadav/whatsapp_msg_cm.com',
    author='Nikil Yadav',
    author_email='nikhil.nikhil2008@gmail.com',
    license='BSD 2-clause',
    #packages=['cm_com_whatsappapi'],
    install_requires=['requests',
                      'json','os'                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)