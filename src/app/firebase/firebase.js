// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";
import { getFirestore } from 'firebase/firestore';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBbVwDx5mQ2gLnb7eRa1xhT6u-47snTRzA",
  authDomain: "saveuserdata-9d1f6.firebaseapp.com",
  projectId: "saveuserdata-9d1f6",
  storageBucket: "saveuserdata-9d1f6.firebasestorage.app",
  messagingSenderId: "327550862731",
  appId: "1:327550862731:web:dab4f3cf22569566221b8e"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getFirestore(app);

// Initialize Firebase Authentication and get a reference to the service
const auth = getAuth(app);

export {app, database, auth,signInWithEmailAndPassword, createUserWithEmailAndPassword};