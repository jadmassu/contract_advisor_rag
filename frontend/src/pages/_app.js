import '@/styles/globals.css'

export default function App({ Component, pageProps }) {
  return <div className="bg-white-200"><Component {...pageProps} /></div>
}
