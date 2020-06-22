
function fileBrowseClick() {
    // on browse button click, divert action to file input selector
    document.getElementById("img-input").click();
}

function showSelectedImage(input) {
    // Show selected input image when user selects one
    // validate input
    if (!isValidFileType(input.files[0])) { return; }
    // update file browse label
    //let imgInputLabel = document.getElementById("img-input-label");
    //imgInputLabel.innerHTML = input.files[0].name;
    // update folder icon
    let folderIcon = document.getElementById("browse-btn-icon");
    folderIcon.classList.remove("fa-folder-open");
    folderIcon.classList.add("fa-folder");
    // update buff button color to bootstrap green
    let buffBtn = document.getElementById("file-submit-btn");
    buffBtn.style.backgroundColor = "#28a745";
    // display input image
    displayImage(input.files[0], "img-original", input.files[0].name);
}

function colorizeImage() {
    // Colorize image on button click
    let input = document.getElementById("img-input");
    // validate input
    if (!isValidFileType(input.files[0])) { return; }
    // display progress indication
    // send image to server
    let request = new XMLHttpRequest();
    let loc = window.location;
    request.open("POST", `${loc.protocol}\/\/${loc.hostname}:${loc.port}/colorizeImage`);
    request.responseType = 'blob';
    request.onload = function(e) {
        if (request.readyState === request.DONE && request.status >= 200 && request.status <= 299) {
            displayImage(e.target.response, "img-new", imgNewAlt);
            // return buff button color to bootstrap blue
            let buffBtn = document.getElementById("file-submit-btn");
            buffBtn.style.backgroundColor = "#007bff";
        } else {
            alert(httpErrorStr);
        }
    }
    request.onerror = function(e) {
        alert(request.responseText);
    }
    let data = new FormData();
    data.append("image", input.files[0]);
    request.send(data);
}

function isValidFileType(file) {
    /*
    validate file/mime type
    parameters: file (bytestream-like) image file
    */
    let ftype = file['type']; // image/png, image/jpeg, text/x...
    if (ftype.split('/')[0] != 'image') {
        alert(invalidImageErrorStr);
        return false;
    }
    return true;
}

function displayImage(file, elementId, alt="") {
    /*
    display image in image element
    parameters: file (bytestream-like) image file
                elementId (string) html image element id
                alt (string) html image element alt attribute text
    */
    let reader = new FileReader();
    reader.onload = function(e) {
        // display image
        let imgElement = document.getElementById(elementId);
        imgElement.src = e.target.result;
        imgElement.alt = alt;
    };
    reader.readAsDataURL(file);
}

function mod(n, m) {
    /*
    This function implements the modulu operator
    JS % is a remainder operator, not a modulu operator
    see https://stackoverflow.com/questions/4467539/javascript-modulo-gives-a-negative-result-for-negative-numbers
    */
    return ((n % m) + m) % m;
}

function cycleCarousel(forward, n) {
    /*
    Cycle through carousel containing example images
    parameters: forward (boolean) - cycle right if true, left if false
                n (int) - number of images in carousel
    */
    let colorImgElement = document.getElementById("img-example-color");
    let grayscaleImgElement = document.getElementById("img-example-grayscale");
    let colorizedImgElement = document.getElementById("img-example-colorized");
    // cycle index
    let idx = colorImgElement.src.charAt(colorImgElement.src.length - 5);
    idx = Number(idx);
    forward ? ++idx : --idx;
    idx = mod(idx, n);
    // update color image
    colorImgElement.src = imgPath + "example_color_" + idx + ".png";
    colorImgElement.alt = exampleColorImgAltPre + idx;
    // update grayscale image
    grayscaleImgElement.src = imgPath + "example_grayscale_" + idx + ".png";
    grayscaleImgElement.alt = exampleGrayscaleImgAltPre + idx;
    // update colorized image
    colorizedImgElement.src = imgPath + "example_colorized_" + idx + ".png";
    colorizedImgElement.alt = exampleColorizedImgAltPre + idx;
}

function selectNetItem(id) {
    let titleElement = document.getElementById("img-net-title");
    let captionElement = document.getElementById("img-net-caption");
    let imgElement = document.getElementById("img-net-chart");
    let citationElement = document.getElementById("img-net-citation");
    switch (id) {
        case "net-select-arch":
            titleElement.innerHTML = netSelectArchTitle;
            captionElement.innerHTML = netSelectArchStr;
            imgElement.src = imgPath + "UNet.png";
            imgElement.alt = netSelectArchImgAlt;
            citationElement.innerHTML = netSelectArchCitation;
            break;
        case "net-select-encoder":
            titleElement.innerHTML = netSelectEncoderTitle;
            captionElement.innerHTML = netSelectEncoderStr;
            imgElement.src = imgPath + "skip_connection.png";
            imgElement.alt = netSelectEncoderImgAlt;
            citationElement.innerHTML = netSelectEncoderCitation;
            break;
        case "net-select-decoder":
            titleElement.innerHTML = netSelectDecoderTitle;
            captionElement.innerHTML = netSelectDecoderStr;
            imgElement.src = imgPath + "visualizing_cnn.png";
            imgElement.alt = netSelectDecoderImgAlt;
            citationElement.innerHTML = netSelectDecoderCitation;
            break;
        case "net-select-train":
            titleElement.innerHTML = netSelectTrainTitle;
            captionElement.innerHTML = netSelectTrainStr;
            imgElement.src = imgPath + "UNet.png";
            imgElement.alt = netSelectTrainImgAlt;
            citationElement.innerHTML = netSelectTrainCitation;
            break;
        case "net-select-data":
            titleElement.innerHTML = netSelectDataTitle;
            captionElement.innerHTML = netSelectDataStr;
            imgElement.src = imgPath + "coco.png";
            imgElement.alt = netSelectDataImgAlt;
            citationElement.innerHTML = netSelectDataCitation;
            break;
        case "net-select-batchnorm":
            titleElement.innerHTML = netSelectNormTitle;
            captionElement.innerHTML = netSelectNormStr;
            imgElement.src = imgPath + "batch_norm_loss.png";
            imgElement.alt = netSelectNormImgAlt;
            citationElement.innerHTML = netSelectNormCitation;
            break;
        case "net-select-chart2":
            titleElement.innerHTML = netSelectChart2Title;
            captionElement.innerHTML = netSelectChart2Str;
            imgElement.src = imgPath + "UNet.png";
            imgElement.alt = netSelectChart2ImgAlt;
            citationElement.innerHTML = netSelectChart2Citation;
            break;
        default:
            break;
    }
}