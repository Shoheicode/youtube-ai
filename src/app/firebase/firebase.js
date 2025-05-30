// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword,signOut } from "firebase/auth";
import { getFirestore, setDoc, doc, collection,getDocs } from 'firebase/firestore';
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
console.log("I AM RUNNING");
const app = initializeApp(firebaseConfig);
const database = getFirestore(app);

// Initialize Firebase Authentication and get a reference to the service
const auth = getAuth(app);

async function signUpWithEmail(email, password) {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    return { user: userCredential.user, error: null };
  } catch (error) {
    if (error.code === "auth/email-already-in-use") {
      return { user: null, error: "An account with this email already exists." };
    } else {
      return { user: null, error: error.message };
    }
  }
}

async function getDataFromDatabase() {
  try {
    if (!auth.currentUser) {
      console.warn("User not logged in");
      return;
    }
    
    const uid = auth.currentUser?.uid;
    console.log(uid);
    if (!uid) {
      console.error("User not logged in");
      return;
    }
    const appearancesRef = collection(database, "users", uid, "appearances");
    const querySnapshot = await getDocs(appearancesRef);
    const data = querySnapshot.docs.map(doc => doc.data());
    console.log(data);
    return data;
  } catch (error) {
    console.error("Error fetching data: ", error);
  }
}

async function addToDatabase(title, channelTitle,publishAt, highlights){
  try {
    const uid = auth.currentUser?.uid;

    if (!uid) {
      console.error("User not logged in");
      return;
    }
    console.log("User ID:", title);
    const appearancesRef = doc(database, "users", uid, "appearances", title);
    // const docRef = await database.collection("users").doc(userId).set(data);
    await setDoc(appearancesRef, {
      title: title,
      publishAt: publishAt,
      channelTitle: channelTitle,
      highlights: highlights,
      createdAt: new Date()
    });

    // console.log("Document written with ID:", docRef.id);
    // console.log("Document written with ID: ", docRef.id);
  } catch (error) {
    console.error("Error adding document: ", error);
  }
}


export {app, addToDatabase, auth,signInWithEmailAndPassword, signUpWithEmail,signOut, createUserWithEmailAndPassword,getDataFromDatabase};