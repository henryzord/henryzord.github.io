# henryzord's personal page

This repository stores the code used to generate the personal webpage https://henryzord.github.io. It uses the 
XML downloaded from my [Lattes CV](https://lattes.cnpq.br/6346810782525797) to generate a graph in 
https://henryzord.github.io/experience. 

This repository also has a GitHub action to run the Python script that generates the graph/renders the HTML pages every
time the code is pushed to remote.

## Setup

Follow these steps to render the website:

```bash
conda create --name personal python=3.10 pip --yes
conda activate personal
conda install --file requirements.txt
```

## Testing preview thumbnails

The Meta (Facebook) ecosystem uses Open Graph to display previews in social media, while Twitter uses Twitter Cards. 
Use https://www.opengraph.xyz/ and https://developers.facebook.com/tools/debug/ to check if your previews are working 
properly.

## Other information

Built with [Boostrap 5.3](https://getbootstrap.com/).



