async function downloadVideo() {
    const videoUrl = document.getElementById('videoUrl').value.trim();
    const statusDiv = document.getElementById('status');
    const downloadLinkDiv = document.getElementById('downloadLink');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // URL validation
    if (!videoUrl || !isValidUrl(videoUrl)) {
        statusDiv.innerHTML = 'Please enter a valid URL';
        statusDiv.className = 'status error';
        return;
    }

    try {
        statusDiv.innerHTML = '';
        downloadLinkDiv.innerHTML = '';
        loadingSpinner.style.display = 'flex';
        loader.style.display = 'block'; // Use the created loader

        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: videoUrl })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to download video');
        }

        // Success handling
        handleSuccessfulDownload(data, downloadLinkDiv, statusDiv);

    } catch (error) {
        handleDownloadError(error, statusDiv);
    } finally {
        loadingSpinner.style.display = 'none';
        loader.style.display = 'none';
    }
}

// Add these helper functions
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function handleSuccessfulDownload(data, downloadLinkDiv, statusDiv) {
    const downloadLink = document.createElement('a');
    downloadLink.href = data.download_url;
    downloadLink.className = 'download-button';
    downloadLink.target = '_blank';
    downloadLink.textContent = `Download ${escapeHtml(data.title)}`;

    downloadLinkDiv.innerHTML = '';
    downloadLinkDiv.appendChild(downloadLink);

    const expirationWarning = document.createElement('p');
    expirationWarning.className = 'expiration-warning';
    expirationWarning.textContent = 'Note: This download link will expire in 1 hour';
    downloadLinkDiv.appendChild(expirationWarning);

    statusDiv.innerHTML = 'Video processed successfully!';
    statusDiv.className = 'status success';
}

function handleDownloadError(error, statusDiv) {
    statusDiv.innerHTML = error.message || 'An error occurred while processing the video';
    statusDiv.className = 'status error';
}