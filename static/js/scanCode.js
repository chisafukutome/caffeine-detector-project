const webcamElement = document.getElementById("webcam");
const canvasElement = document.getElementById("canvas");
const snapshotBtn = document.getElementById("snapshot-btn");
const scanFeedback = document.getElementById("scanFeedback");

const webcam = new Webcam(webcamElement, "user", canvasElement);

webcam
  .start()
  .then((result) => {
    console.log("webcam started");
  })
  .catch((err) => {
    console.log(err);
  });

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

function redirectToReceipt(resData) {
  console.log("RESPONSE: ", resData);

  if (resData["status"] == "Barcode found, processing...") {
    const productName = resData["productName"];
    const urlWithProductName = "/receipt/<" + productName + ">";
    window.location.href = urlWithProductName;
  } else if (resData["status"] == "Barcode not found") {
    giveScanFeedback("Barcode not found");
  } else if (resData["status"] == "Product not found") {
    giveScanFeedback("Product not found");
  } else if (resData["status"] == "Failed to read barcode") {
    giveScanFeedback("Failed to read barcode");
  }
}

function giveScanFeedback(statusMsg) {
  scanFeedback.style.visibility = "visible";
  scanFeedback.innerText = statusMsg;
}
