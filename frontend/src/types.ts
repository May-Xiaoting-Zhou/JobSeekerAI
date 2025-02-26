export interface Message {
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

// Add an empty export to make it a module
export {}; 