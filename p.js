function callit() {
    console.log("hello");
}

let intervalId; // Store the interval ID here

const time = () => {
    intervalId = setInterval(() => {
        callit();
    }, 1000);
    return intervalId; // Return the ID (optional)
}

// Start the interval
time();

setTimeout(() => {
    clearInterval(intervalId); // Clear using the stored ID
}, 5000);