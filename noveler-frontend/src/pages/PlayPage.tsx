import React from 'react';
import Header from '../components/StorytellingMode/Header';
import NarrativePane from '../components/StorytellingMode/NarrativePane';
import UserInputComponent from '../components/StorytellingMode/UserInputComponent';
import ActionsMenu from '../components/StorytellingMode/ActionsMenu';

const PlayPage: React.FC = () => {
  return (
    <div className="flex flex-col">
      <Header />
      <NarrativePane />
      <UserInputComponent />
      <ActionsMenu />
    </div>
  );
};

export default PlayPage;