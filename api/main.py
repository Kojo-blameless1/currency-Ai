from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn as nn
import numpy as np
import pickle
from PIL import Image
import io

# ── Model Architecture ─────────────────────────────────────────────────
class CurrencyClassifier(nn.Module):
    def __init__(self, input_size=256, num_classes=10):
        super(CurrencyClassifier, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        return self.network(x)

# ── Load Model & Label Encoder ─────────────────────────────────────────
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = CurrencyClassifier(input_size=256, num_classes=10).to(device)
model.load_state_dict(torch.load('models/best_model.pth', map_location=device))
model.eval()

with open('models/label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

print("Model loaded successfully ✅")

# ── Load MobileNetV2 as our encoder (replaces Microsoft's encoder) ─────
import torchvision.models as models
import torchvision.transforms as transforms

mobilenet = models.mobilenet_v2(weights='IMAGENET1K_V1')
mobilenet.classifier = nn.Identity()  # Remove classification head
mobilenet = mobilenet.to(device)
mobilenet.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

print("Encoder loaded successfully ✅")

# ── FastAPI App ────────────────────────────────────────────────────────
app = FastAPI(title="Currency AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read and preprocess image
    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img_tensor = transform(img).unsqueeze(0).to(device)

    # Extract features using MobileNetV2
    with torch.no_grad():
        features = mobilenet(img_tensor)  # shape: (1, 1280)
        
        # Reduce 1280 → 256 to match our trained model
        features = features[:, :256]  # take first 256 features

    # Classify currency
    with torch.no_grad():
        outputs = model(features)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    currency = le.inverse_transform(predicted.cpu().numpy())[0]
    confidence_score = confidence.item() * 100

    return {
        "currency": currency,
        "confidence": f"{confidence_score:.2f}%",
        "status": "success"
    }