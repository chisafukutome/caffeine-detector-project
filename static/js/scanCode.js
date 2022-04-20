const webcamElement = document.getElementById("webcam");
const canvasElement = document.getElementById("canvas");
const snapshotBtn = document.getElementById("snapshot-btn");
const scanFeedback = document.getElementById("scanFeedback");

//initialize webcam
const webcam = new Webcam(webcamElement, "user", canvasElement);
webcam
  .start()
  .then((result) => {
    console.log("webcam started");
  })
  .catch((err) => {
    console.log(err);
  });

//take webcam snapshot to scan for barcode
snapshotBtn.addEventListener("click", (e) => {
  let picture = webcam.snap();

  giveScanFeedback("Processing...");

  postBarcodeImg("/scanCode", picture)
    .then((res) => res.json())
    .then((resData) => {
      redirectToReceipt(resData);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

//request server to find information based on scanned barcode
async function postBarcodeImg(url = "", data = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data.replace(`data:image/png;base64,`, "")),
  });
  return response;
}

//actions depending on success of information lookup based on scanned barcode
function redirectToReceipt(resData) {
  console.log("RESPONSE: ", resData);

  if (resData["status"] == "Barcode found, processing...") {
    //redirect if successful
    const productName = resData["productName"];
    const urlWithProductName = "/receipt/<" + productName + ">";
    window.location.href = urlWithProductName;
  } else if (resData["status"] == "Barcode not found") {
    //indicate no barcode found
    giveScanFeedback("Barcode not found");
  } else if (resData["status"] == "Product not found") {
    //indicate barcode found, but not product
    giveScanFeedback("Product not found");
  } else if (resData["status"] == "Failed to read barcode") {
    //indicate general failure to scan barcode
    giveScanFeedback("Failed to read barcode");
  }
}

//create alert on scan page to give feedback on status of barcode search
function giveScanFeedback(statusMsg) {
  scanFeedback.style.visibility = "visible";
  scanFeedback.innerText = statusMsg;
}
