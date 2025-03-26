import { create } from 'zustand';

interface ModelingObject {
  id: string;
  name: string;
  description?: string;
  inheritance?: string;
  composition: {
    hierarchical: string[];
    lateral: string[];
  };
  links: { id: string; type: 'hierarchical' | 'lateral' }[];
  properties: { key: string; value: any }[];
  sections: { title: string; content: any }[];
}

interface Story {
  id: string;
  scenario?: string;
  title?: string;
  entries: {
    id: string;
    text: string;
    branchPoint?: boolean;
    children?: any[];
  }[];
}

interface StoreState {
  modeling: { [key: string]: ModelingObject[] };
  stories: { [key: string]: Story };
  ui: {
    selectedObject?: ModelingObject;
    selectedStory?: Story;
    showModal: boolean;
    modalType?: string;
    errorMessage?: string;
    successMessage?: string;
  };
  setModelingObjects: (objectType: string, objects: ModelingObject[]) => void;
  setStories: (storyId: string, story: Story) => void;
  setUIState: (uiState: Partial<StoreState['ui']>) => void;
}

const useStore = create<StoreState>((set) => ({
  modeling: {},
  stories: {},
  ui: {
    showModal: false,
  },
  setModelingObjects: (objectType, objects) =>
    set((state) => ({
      modeling: {
        ...state.modeling,
        [objectType]: objects,
      },
    })),
  setStories: (storyId, story) =>
    set((state) => ({
      stories: {
        ...state.stories,
        [storyId]: story,
      },
    })),
  setUIState: (uiState) =>
    set((state) => ({
      ui: {
        ...state.ui,
        ...uiState,
      },
    })),
}));

export default useStore;