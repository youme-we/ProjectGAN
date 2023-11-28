![alt text](https://www.yankodesign.com/images/design_news/2023/02/ai-generates-eye-popping-car-designs-in-the-style-of-famous-architects/Moss-and-Fog-Renzo-Piano.jpg)

# ProjectGAN

ProjectGAN consists of a GAN which can be managed and analysed by an embodied UI. A GAN is a NeuroanlNetwork specificaly developed to create Data. In this case it is creating Images from random noise. 



## Deployment
#### To run the GAN on its own without using the UI run the following command in the main direcotry:

```bash
  make run 
```

#### To run the GAN with its correspoinding UI run the following command:

```bash
  make plot 
```

#### Change parameters of the NN

##### go into the parameters.json file 
##### here you can for example change the origin of your dataset
##### To compress and make use of your data with the stated orignin, run following command

```bash
  make compress
```

