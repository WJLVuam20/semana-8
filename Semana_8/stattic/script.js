let isRecording = false;
let mediaRecorder = null;
let audioChunks = [];

const recordButton = document.getElementById('recordButton');
const transcriptionDiv = document.getElementById('transcription');

// Function to convert audio blob to PCM WAV
async function convertToWav(blob) {
    const arrayBuffer = await blob.arrayBuffer();
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    // Create WAV file
    const wavBuffer = audioBufferToWav(audioBuffer);
    return new Blob([wavBuffer], { type: 'audio/wav' });
}

// Function to convert AudioBuffer to WAV (simplified WAV encoder)
function audioBufferToWav(buffer) {
    const numChannels = buffer.numberOfChannels;
    const sampleRate = buffer.sampleRate;
    const format = 1; // PCM
    const bitDepth = 16;
    const bytesPerSample = bitDepth / 8;
    const blockAlign = numChannels * bytesPerSample;

    const dataLength = buffer.length * numChannels * bytesPerSample;
    const bufferOut = new ArrayBuffer(44 + dataLength);
    const view = new DataView(bufferOut);

    // Write WAV header
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + dataLength, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint16(16, 16, true);
    view.setUint16(20, format, true);
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * blockAlign, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, bitDepth, true);
    writeString(view, 36, 'data');
    view.setUint32(40, dataLength, true);

    // Write PCM samples
    const length = buffer.length;
    let offset = 44;
    for (let i = 0; i < length; i++) {
        for (let channel = 0; channel < numChannels; channel++) {
            const sample = buffer.getChannelData(channel)[i];
            const value = Math.max(-1, Math.min(1, sample)) * 0x7FFF;
            view.setInt16(offset, value, true);
            offset += 2;
        }
    }

    return bufferOut;
}

function writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
    }
}

recordButton.addEventListener('click', async () => {
    if (!isRecording) {
        // Start recording
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' }); // Use webm for broader compatibility
            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                let audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                
                try {
                    // Convert to WAV
                    audioBlob = await convertToWav(audioBlob);
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'recording.wav');

                    // Send audio to server
                    const response = await fetch('/transcribe', {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();

                    if (result.text) {
                        transcriptionDiv.textContent = result.text;
                    } else {
                        transcriptionDiv.textContent = 'Error: ' + result.error;
                    }
                } catch (err) {
                    transcriptionDiv.textContent = 'Error processing audio: ' + err.message;
                }
            };

            mediaRecorder.start();
            recordButton.textContent = 'Stop Recording';
            recordButton.classList.add('recording');
            isRecording = true;
        } catch (err) {
            transcriptionDiv.textContent = 'Error accessing microphone: ' + err.message;
        }
    } else {
        // Stop recording
        mediaRecorder.stop();
        recordButton.textContent = 'Start Recording';
        recordButton.classList.remove('recording');
        isRecording = false;
    }
});