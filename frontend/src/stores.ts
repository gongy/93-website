// src/stores/content.js
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

const stored = localStorage.getItem("userToken");

export const userToken: Writable<string> = writable(stored || "");

userToken.subscribe((value) => localStorage.setItem("userToken", value))