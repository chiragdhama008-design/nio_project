import React, { useState } from 'react';
import { processReport } from '../services/mockApi';

export default function CitizenForm({ onReportSubmitted }) {
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Create a fake preview URL for demo purposes
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description || !location) {
      alert('Please fill out the description and location.');
      return;
    }

    setIsSubmitting(true);
    
    // Process via mock AI pipeline
    const result = await processReport({ description, location, imagePreview });
    
    setIsSubmitting(false);
    onReportSubmitted(result);
    
    // Reset form
    setDescription('');
    setLocation('');
    setImagePreview(null);
    e.target.reset();
  };

  return (
    <div className="citizen-form-container">
      <h2>Report a Hazard</h2>
      <p className="subtitle">CivicShield automatically analyzes and prioritizes your report.</p>
      
      <form onSubmit={handleSubmit} className="citizen-form">
        <div className="form-group">
          <label>Location</label>
          <input 
            type="text" 
            placeholder="e.g. 123 Main St crosswalk" 
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            disabled={isSubmitting}
          />
        </div>

        <div className="form-group">
          <label>Description</label>
          <textarea 
            placeholder="Describe the hazard (e.g. Huge pothole causing dangerous swerving)..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="4"
            disabled={isSubmitting}
          />
        </div>

        <div className="form-group">
          <label>Upload Photo</label>
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleImageChange}
            disabled={isSubmitting}
          />
          {imagePreview && (
            <div className="image-preview">
              <img src={imagePreview} alt="Hazard preview" />
            </div>
          )}
        </div>

        <button type="submit" disabled={isSubmitting} className="submit-btn">
          {isSubmitting ? 'Analyzing with AI...' : 'Submit Report'}
        </button>
      </form>
    </div>
  );
}
