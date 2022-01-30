const webcamElement = document.getElementById("webcam");
const canvasElement = document.getElementById("canvas");
//const snapSoundElement = document.getElementById("snapSound");
const snapshotBtn = document.getElementById("snapshot-btn");

const webcam = new Webcam(
  webcamElement,
  "user",
  canvasElement
  //snapSoundElement
);

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
  console.log(picture);
  document.querySelector("#canvas").href = picture;
  console.log("Snapshot taken");

  getPotentialBarcodeImg("/", picture)
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

async function getPotentialBarcodeImg(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(data.replace(`data:image/png;base64,`, "")), // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}
