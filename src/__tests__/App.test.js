import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import App from '../App';

beforeEach(() => {
  localStorage.clear();
});

test('toggles theme from light to dark', () => {
  const { getByText } = render(<App />);
  const button = getByText('Toggle Theme');

  // Initial theme should be light
  expect(document.body.className).toBe('light');

  // Toggle to dark
  fireEvent.click(button);
  expect(document.body.className).toBe('dark');
  expect(localStorage.getItem('theme')).toBe('dark');

  // Toggle back to light
  fireEvent.click(button);
  expect(document.body.className).toBe('light');
  expect(localStorage.getItem('theme')).toBe('light');
});


test('applies saved theme from localStorage on load', () => {
  localStorage.setItem('theme', 'dark');
  render(<App />);
  expect(document.body.className).toBe('dark');
});
