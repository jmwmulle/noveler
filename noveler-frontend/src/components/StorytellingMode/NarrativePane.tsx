import React from 'react';
import useStore from '../../store/useStore';

const NarrativePane: React.FC = () => {
  const selectedStory = useStore((state) => state.ui.selectedStory);

  if (!selectedStory) {
    return <div className="flex-1 p-4">No story selected</div>;
  }

  return (
    <div className="flex-1 p-4">
      <h2 className="text-xl mb-4">{selectedStory.title}</h2>
      <div>
        {selectedStory.entries.map((entry) => (
          <div key={entry.id} className="mb-4">
            <p>{entry.text}</p>
            {entry.branchPoint && (
              <div className="ml-4">
                {entry.children?.map((child) => (
                  <div key={child.id} className="mb-2">
                    <p>{child.text}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default NarrativePane;