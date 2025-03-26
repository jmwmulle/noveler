import React, { useState } from 'react';
import useStore from '../../store/useStore';

const AnnotationModal: React.FC = () => {
  const [annotation, setAnnotation] = useState('');
  const selectedStory = useStore((state) => state.ui.selectedStory);
  const setUIState = useStore((state) => state.setUIState);

  const handleSubmit = () => {
    if (!selectedStory) return;

    const newEntry = {
      id: Date.now().toString(),
      text: annotation,
      branchPoint: false,
      children: [],
    };

    const updatedEntries = [...selectedStory.entries, newEntry];
    const updatedStory = { ...selectedStory, entries: updatedEntries };

    fetch(`/story/${selectedStory.id}/annotate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newEntry),
    }).then((response) => response.json());

    setUIState({ showModal: false });
  };

  const handleClose = () => {
    setUIState({ showModal: false });
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-4 rounded">
        <h2 className="text-xl mb-4">Annotation Modal</h2>
        <textarea
          value={annotation}
          onChange={(e) => setAnnotation(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded mb-2"
        />
        <div className="flex space-x-4">
          <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleSubmit}>
            Submit
          </button>
          <button className="bg-gray-500 text-white px-4 py-2 rounded" onClick={handleClose}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default AnnotationModal;