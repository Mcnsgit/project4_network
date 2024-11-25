// Utility Functions
function getCSRFToken() {
    const token = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    if (!token) throw new Error('CSRF token not found');
    return token;
}

function showLoading(element) {
    element.classList.add('loading');
    element.setAttribute('disabled', true);
    element.originalText = element.innerHTML;
    element.innerHTML = '<span class="spinner"></span>';
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.removeAttribute('disabled');
    element.innerHTML = element.originalText;
}

function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container') || (() => {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    })();

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-header">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
            <strong class="me-auto">${type === 'success' ? 'Success' : 'Error'}</strong>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
        <div class="toast-body">${message}</div>
    `;

    toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Error Handling
async function handleApiError(error, fallbackMessage) {
    console.error('API Error:', error);
    let errorMessage = fallbackMessage;
    
    if (error.response) {
        try {
            const data = await error.response.json();
            errorMessage = data.error || fallbackMessage;
        } catch (e) {
            errorMessage = error.response.statusText || fallbackMessage;
        }
    }
    
    showToast(errorMessage, 'danger');
    throw new Error(errorMessage);
}

// Post Management
async function editPost(postId) {
    const postDiv = document.getElementById(`post-${postId}`);
    if (!postDiv) throw new Error('Post element not found');
    
    const postContent = postDiv.querySelector('.post-content')?.innerText;
    const originalHtml = postDiv.innerHTML;

    try {
        postDiv.innerHTML = `
            <div class="edit-post-form">
                <textarea class="form-control mb-2" id="edit-content-${postId}">${postContent || ''}</textarea>
                <div class="d-flex justify-content-end gap-2">
                    <button class="btn btn-secondary" onclick="cancelEdit(${postId}, '${encodeURIComponent(originalHtml)}')">
                        <i class="fas fa-times me-1"></i>Cancel
                    </button>
                    <button class="btn btn-primary" onclick="savePost(${postId})">
                        <i class="fas fa-save me-1"></i>Save
                    </button>
                </div>
            </div>
        `;
    } catch (error) {
        handleApiError(error, 'Error preparing edit form');
    }
}

function cancelEdit(postId, originalHtml) {
    const postDiv = document.getElementById(`post-${postId}`);
    if (!postDiv) return;
    postDiv.innerHTML = decodeURIComponent(originalHtml);
}

async function savePost(postId) {
    const editButton = document.querySelector(`#post-${postId} .btn-primary`);
    const editContent = document.getElementById(`edit-content-${postId}`)?.value;
    
    if (!editContent?.trim()) {
        showToast('Post content cannot be empty', 'danger');
        return;
    }

    showLoading(editButton);

    try {
        const response = await fetch(`/update_post/${postId}/`, {
            method: 'POST',
            body: JSON.stringify({ content: editContent }),
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Failed to update post');

        const data = await response.json();
        
        document.getElementById(`post-${postId}`).innerHTML = `
            <div class="post-content">${data.content || editContent}</div>
            <div class="post-footer">
                <button class="btn btn-outline-primary btn-sm" onclick="editPost(${postId})">
                    <i class="fas fa-edit me-1"></i>Edit
                </button>
            </div>
        `;
        showToast('Post updated successfully');
    } catch (error) {
        handleApiError(error, 'Failed to update post');
    } finally {
        hideLoading(editButton);
    }
}

// Like Management
async function toggleLike(postId) {
    const likeButton = document.getElementById(`like-btn-${postId}`);
    if (!likeButton) return;

    showLoading(likeButton);

    try {
        const response = await fetch(`/toggle_like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Failed to toggle like');

        const data = await response.json();
        
        const likeCount = document.getElementById(`like-count-${postId}`);
        if (likeCount) likeCount.textContent = data.likes_count;
        
        likeButton.innerHTML = `
            <i class="fas fa-${data.is_liked ? 'heart' : 'heart-o'}"></i>
            ${data.is_liked ? 'Unlike' : 'Like'}
        `;
        
        showToast(data.is_liked ? 'Post liked!' : 'Post unliked');
    } catch (error) {
        handleApiError(error, 'Failed to toggle like');
    } finally {
        hideLoading(likeButton);
    }
}

// Comment Management
async function toggleComments(postId) {
    const commentsSection = document.getElementById(`comments-${postId}`);
    const toggleButton = document.getElementById(`toggle-comments-${postId}`);
    
    if (commentsSection.style.display === 'none') {
        showLoading(toggleButton);
        try {
            const response = await fetch(`/post/${postId}/comments/`);
            const data = await response.json();
            
            if (!response.ok) throw new Error(data.error || 'Failed to load comments');
            
            commentsSection.innerHTML = data.comments.map(comment => `
                <div class="comment mb-2">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <strong>${comment.author}</strong>
                            <small class="text-muted ms-2">${comment.date}</small>
                        </div>
                        ${comment.can_delete ? `
                            <button class="btn btn-link btn-sm text-danger" onclick="deleteComment(${comment.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        ` : ''}
                    </div>
                    <div>${comment.content}</div>
                </div>
            `).join('') || '<p class="text-muted">No comments yet</p>';
            
            commentsSection.style.display = 'block';
            toggleButton.innerHTML = '<i class="fas fa-chevron-up me-1"></i>Hide Comments';
        } catch (error) {
            handleApiError(error, 'Failed to load comments');
        } finally {
            hideLoading(toggleButton);
        }
    } else {
        commentsSection.style.display = 'none';
        toggleButton.innerHTML = '<i class="fas fa-chevron-down me-1"></i>Show Comments';
    }
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add loading overlay for initial page load
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'loading-overlay';
        loadingOverlay.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
        mainContent.appendChild(loadingOverlay);
        
        // Remove loading overlay once content is loaded
        window.addEventListener('load', () => {
            loadingOverlay.style.opacity = '0';
            setTimeout(() => loadingOverlay.remove(), 300);
        });
    }

    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});