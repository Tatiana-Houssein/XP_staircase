import { createFeatureSelector, createSelector } from '@ngrx/store';

export interface AppState {
  isExperimentLaunched: boolean;
  currentId: number;
  currentName: string;
  nextId: number;
}

export const initialState: AppState = {
  isExperimentLaunched: false,
  currentId: 1,
  currentName: 'Initial Name',
  nextId: 2,
};

// Feature Selector
export const selectAppState = createFeatureSelector<AppState>('app');

// Selectors
export const selectCurrentId = createSelector(selectAppState, (state) => state.currentId);

export const selectNextId = createSelector(selectAppState, (state) => state.nextId);

export const selectIsExperimentLaunched = createSelector(selectAppState, (state) => state.isExperimentLaunched);
