export type Unit = 'kg' | 'lbs';

export const kgToLbs = (kg: number): number => kg * 2.20462;
export const lbsToKg = (lbs: number): number => lbs / 2.20462;

export interface Reading {
  id: number;
  date: string;
  mass: string;
}

export interface FormDataWithUnit {
  date: string;
  mass: string;
  unit: Unit;
}