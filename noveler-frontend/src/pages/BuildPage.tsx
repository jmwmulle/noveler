import React from 'react';
import MenuSection from '../components/ModelingMode/MenuSection';
import ListSection from '../components/ModelingMode/ListSection';
import EditorPane from '../components/ModelingMode/EditorPane';
import ActionsPane from '../components/ModelingMode/ActionsPane';
import LinksSection from '../components/ModelingMode/LinksSection';

const BuildPage: React.FC = () => {
  return (
    <div className="flex">
      <MenuSection />
      <ListSection />
      <EditorPane />
      <ActionsPane />
      <LinksSection />
    </div>
  );
};

export default BuildPage;