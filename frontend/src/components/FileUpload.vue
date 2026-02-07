<template>
  <div class="file-upload">
    <div class="upload-area" 
         :class="{ 'dragover': isDragOver, 'uploading': uploading }"
         @drop="handleDrop"
         @dragover.prevent="isDragOver = true"
         @dragleave="isDragOver = false"
         @dragenter.prevent>
      
      <div class="upload-content">
        <div v-if="!uploading" class="text-center">
          <i class="bi bi-cloud-upload display-4 text-muted mb-3"></i>
          <h5 class="mb-3">Drop files here or click to upload</h5>
          <p class="text-muted mb-3">
            Supported formats: {{ allowedTypes.join(', ') }}<br>
            Maximum file size: {{ maxFileSizeMB }}MB
          </p>
          <input ref="fileInput" 
                 type="file" 
                 :accept="acceptTypes"
                 :multiple="multiple"
                 @change="handleFileSelect"
                 class="d-none">
          <button @click="$refs.fileInput.click()" 
                  class="btn btn-primary me-2">
            <i class="bi bi-folder2-open me-2"></i>
            Browse Files
          </button>
          <button v-if="showCamera" @click="openCamera" 
                  class="btn btn-outline-primary">
            <i class="bi bi-camera me-2"></i>
            Take Photo
          </button>
        </div>
        
        <div v-else class="text-center">
          <div class="spinner-border text-primary mb-3" role="status">
            <span class="visually-hidden">Uploading...</span>
          </div>
          <h5>Uploading files...</h5>
          <div class="progress mb-3">
            <div class="progress-bar" 
                 :style="{ width: uploadProgress + '%' }"
                 role="progressbar">
              {{ uploadProgress }}%
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- File Preview -->
    <div v-if="files.length > 0" class="mt-4">
      <h6 class="mb-3">Files to upload:</h6>
      <div class="file-list">
        <div v-for="(file, index) in files" :key="index" class="file-item">
          <div class="d-flex align-items-center">
            <div class="file-icon me-3">
              <i :class="getFileIcon(file.type)" class="fs-4"></i>
            </div>
            <div class="file-info flex-grow-1">
              <div class="file-name">{{ file.name }}</div>
              <div class="file-meta text-muted small">
                {{ formatFileSize(file.size) }} • {{ file.type }}
              </div>
            </div>
            <div class="file-actions">
              <button @click="removeFile(index)" 
                      class="btn btn-sm btn-outline-danger">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>
          
          <!-- Preview for images -->
          <div v-if="isImage(file)" class="mt-2">
            <img :src="file.preview" 
                 :alt="file.name"
                 class="img-thumbnail"
                 style="max-height: 100px; max-width: 150px;">
          </div>
        </div>
      </div>
      
      <div class="mt-3">
        <button @click="uploadFiles" 
                :disabled="uploading || files.length === 0"
                class="btn btn-success me-2">
          <i class="bi bi-upload me-2"></i>
          Upload {{ files.length }} File{{ files.length > 1 ? 's' : '' }}
        </button>
        <button @click="clearFiles" 
                :disabled="uploading"
                class="btn btn-outline-secondary">
          <i class="bi bi-x-circle me-2"></i>
          Clear All
        </button>
      </div>
    </div>

    <!-- Upload Results -->
    <div v-if="uploadResults.length > 0" class="mt-4">
      <h6 class="mb-3">Upload Results:</h6>
      <div class="results-list">
        <div v-for="(result, index) in uploadResults" :key="index" 
             :class="['result-item', result.success ? 'success' : 'error']">
          <div class="d-flex align-items-center">
            <div class="result-icon me-3">
              <i :class="result.success ? 'bi-check-circle-fill text-success' : 'bi-x-circle-fill text-danger'"></i>
            </div>
            <div class="result-info flex-grow-1">
              <div class="result-name">{{ result.fileName }}</div>
              <div v-if="result.message" class="result-message text-muted small">
                {{ result.message }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'FileUpload',
  props: {
    multiple: {
      type: Boolean,
      default: false
    },
    maxFiles: {
      type: Number,
      default: 5
    },
    maxFileSizeMB: {
      type: Number,
      default: 5
    },
    allowedTypes: {
      type: Array,
      default: () => ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'application/pdf', 'text/plain']
    },
    showCamera: {
      type: Boolean,
      default: false
    },
    uploadUrl: {
      type: String,
      required: true
    },
    additionalData: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['upload-success', 'upload-error', 'upload-progress'],
  setup(props, { emit }) {
    const fileInput = ref(null)
    const files = ref([])
    const isDragOver = ref(false)
    const uploading = ref(false)
    const uploadProgress = ref(0)
    const uploadResults = ref([])

    const acceptTypes = computed(() => {
      return props.allowedTypes.join(',')
    })

    const maxFileSizeBytes = computed(() => {
      return props.maxFileSizeMB * 1024 * 1024
    })

    const handleFileSelect = (event) => {
      const selectedFiles = Array.from(event.target.files)
      addFiles(selectedFiles)
    }

    const handleDrop = (event) => {
      event.preventDefault()
      isDragOver.value = false
      
      const droppedFiles = Array.from(event.dataTransfer.files)
      addFiles(droppedFiles)
    }

    const addFiles = (newFiles) => {
      const validFiles = newFiles.filter(file => {
        // Check file type
        if (!props.allowedTypes.includes(file.type)) {
          uploadResults.value.push({
            fileName: file.name,
            success: false,
            message: `Invalid file type: ${file.type}`
          })
          return false
        }
        
        // Check file size
        if (file.size > maxFileSizeBytes.value) {
          uploadResults.value.push({
            fileName: file.name,
            success: false,
            message: `File too large: ${formatFileSize(file.size)} (max: ${props.maxFileSizeMB}MB)`
          })
          return false
        }
        
        return true
      })

      // Check max files limit
      const remainingSlots = props.maxFiles - files.value.length
      const filesToAdd = validFiles.slice(0, remainingSlots)
      
      if (remainingSlots < validFiles.length) {
        uploadResults.value.push({
          fileName: 'System',
          success: false,
          message: `Only ${remainingSlots} more files allowed (max: ${props.maxFiles})`
        })
      }

      // Add preview for images
      filesToAdd.forEach(file => {
        if (isImage(file)) {
          file.preview = URL.createObjectURL(file)
        }
      })

      files.value.push(...filesToAdd)
    }

    const removeFile = (index) => {
      const file = files.value[index]
      if (file.preview) {
        URL.revokeObjectURL(file.preview)
      }
      files.value.splice(index, 1)
    }

    const clearFiles = () => {
      files.value.forEach(file => {
        if (file.preview) {
          URL.revokeObjectURL(file.preview)
        }
      })
      files.value = []
      uploadResults.value = []
    }

    const uploadFiles = async () => {
      if (files.value.length === 0) return

      uploading.value = true
      uploadProgress.value = 0
      uploadResults.value = []

      try {
        const formData = new FormData()
        
        // Add files
        if (props.multiple) {
          files.value.forEach((file, index) => {
            formData.append(`files[${index}]`, file)
          })
        } else {
          formData.append('file', files.value[0])
        }

        // Add additional data
        Object.entries(props.additionalData).forEach(([key, value]) => {
          formData.append(key, value)
        })

        const response = await fetch(props.uploadUrl, {
          method: 'POST',
          body: formData,
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })

        if (response.ok) {
          const result = await response.json()
          
          files.value.forEach(file => {
            uploadResults.value.push({
              fileName: file.name,
              success: true,
              message: 'Upload successful'
            })
          })

          emit('upload-success', result)
          clearFiles()
        } else {
          const error = await response.json()
          
          files.value.forEach(file => {
            uploadResults.value.push({
              fileName: file.name,
              success: false,
              message: error.message || 'Upload failed'
            })
          })

          emit('upload-error', error)
        }
      } catch (error) {
        files.value.forEach(file => {
          uploadResults.value.push({
            fileName: file.name,
            success: false,
            message: error.message || 'Network error'
          })
        })

        emit('upload-error', error)
      } finally {
        uploading.value = false
        uploadProgress.value = 0
      }
    }

    const openCamera = () => {
      // Create camera input
      const cameraInput = document.createElement('input')
      cameraInput.type = 'file'
      cameraInput.accept = 'image/*'
      cameraInput.capture = 'environment'
      
      cameraInput.onchange = (event) => {
        const file = event.target.files[0]
        if (file) {
          addFiles([file])
        }
      }
      
      cameraInput.click()
    }

    const isImage = (file) => {
      return file.type.startsWith('image/')
    }

    const getFileIcon = (fileType) => {
      if (fileType.startsWith('image/')) {
        return 'bi-file-image text-primary'
      } else if (fileType === 'application/pdf') {
        return 'bi-file-pdf text-danger'
      } else if (fileType.startsWith('text/')) {
        return 'bi-file-text text-info'
      } else {
        return 'bi-file-earmark text-secondary'
      }
    }

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }

    return {
      fileInput,
      files,
      isDragOver,
      uploading,
      uploadProgress,
      uploadResults,
      acceptTypes,
      handleFileSelect,
      handleDrop,
      removeFile,
      clearFiles,
      uploadFiles,
      openCamera,
      isImage,
      getFileIcon,
      formatFileSize
    }
  }
}
</script>

<style scoped>
.file-upload {
  width: 100%;
}

.upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 0.75rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

.upload-area:hover {
  border-color: #0d6efd;
  background-color: #f0f8ff;
}

.upload-area.dragover {
  border-color: #0d6efd;
  background-color: #e7f3ff;
  transform: scale(1.02);
}

.upload-area.uploading {
  border-color: #6c757d;
  background-color: #f8f9fa;
}

.file-list {
  max-height: 300px;
  overflow-y: auto;
}

.file-item {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 0.5rem;
  background-color: white;
}

.file-icon {
  width: 40px;
  text-align: center;
}

.file-name {
  font-weight: 500;
}

.results-list {
  max-height: 200px;
  overflow-y: auto;
}

.result-item {
  padding: 0.5rem;
  border-radius: 0.25rem;
  margin-bottom: 0.25rem;
}

.result-item.success {
  background-color: #d4edda;
}

.result-item.error {
  background-color: #f8d7da;
}

.img-thumbnail {
  border-radius: 0.25rem;
}

.progress {
  height: 0.5rem;
}
</style>
