/* Paths */
var imgPath = "/resources/";

/* Buff section */
var httpErrorStr = "Something went wrong!";
var invalidImageErrorStr = "That is not a valid image file type!";

var imgNewAlt = "Colorized image";

/* Examples section */
var exampleColorImgAltPre = "Example color image ";
var exampleGrayscaleImgAltPre = "Example grayscale image ";
var exampleColorizedImgAltPre = "Example colorized image ";

/* Net section */
var netSelectArchTitle = "UNet Architecture";
var netSelectArchStr = "ImgBuff uses a neural network to colorize images. The neural network uses a UNet architecture. The network first breaks down an image into patterns using an 'encoder', then rebuilds a new image with an analog structure called a 'decoder'.";
var netSelectArchImgAlt = "UNet neural network architecture diagram";
var netSelectArchCitation = "Source: Ronneberger, O., Fischer, P., & Brox, T. (2015). <em>U-Net: Convolutional Networks for Biomedical Image Segmentation.</em>";

var netSelectEncoderTitle = "ResNet Encoder";
var netSelectEncoderStr = "The ImgBuff encoder is based on the ResNet architecture. The major innovation of ResNet is the use of a skip connection. A skip connection prevents overfitting by parameterizing the weighted sum of a network layer’s output with its input features; the output of such a layer influences the model only to the extent that it offers improvement over its input.";
var netSelectEncoderImgAlt = "ResNet skip connection diagram";
var netSelectEncoderCitation = "Source: He, K., Zhang, X., Ren, S., & Sun, J. (2015). <em>Deep Residual Learning for Image Recognition.</em>";

var netSelectDecoderTitle = "Decoder";
var netSelectDecoderStr = "While the encoder learns visual patterns, the decoder uses those patterns to rebuild coherent images. The ImgBuff model learns which colors to apply to which patterns.";
var netSelectDecoderImgAlt = "Visualizing Convolutional Neural Networks graphic";
var netSelectDecoderCitation = "Source: Zeiler, M. D., & Fergus, R. (2013). <em>Visualizing and Understanding Convolutional Networks.";

var netSelectTrainTitle = "Training";
var netSelectTrainStr = "2 Lorem ipsum dolor sit amet, purto scripta invidunt duo eu. Nec laudem complectitur ei, diam prima placerat ne eum, te perfecto legendos necessitatibus mei. Pro id delenit maiorum democritum. Laudem facete nominati cu quo, sit menandri definitiones ea. Mea cu corpora vivendum necessitatibus, mea ipsum lobortis definiebas ex, sea munere delicatissimi id.";
var netSelectTrainImgAlt = "";
var netSelectTrainCitation = "Created by author using FastAI library";

var netSelectDataTitle = "COCO Dataset";
var netSelectDataStr = "The neural network is trained using a 118,000 image subset of the Common Objects in Context (COCO) dataset. COCO is a rich, diverse collection of everyday photos taken by ordinary people and uploaded to Flickr.";
var netSelectDataImgAlt = "COCO dataset summary";
var netSelectDataCitation = "Source: http://cocodataset.org/";

var netSelectNormTitle = "Batch Normalization";
var netSelectNormStr = "ResNet makes heavy use of batch normalization. A batch normalization layer standardizes the output of an activation layer to have zero mean and unit variance. This smooths the loss gradient, facilitating convergence to a better optimum.";
var netSelectNormImgAlt = "Batch normalization diagram";
var netSelectNormCitation = "Source: Santurkar, S., Tsipras, D., Ilyas, A., & Madry, A. (2019). <em>How Does Batch Normalization Help Optimization?</em>"


