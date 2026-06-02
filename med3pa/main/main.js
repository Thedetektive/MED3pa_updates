import path from 'path'
import { app, ipcMain } from 'electron'
import serve from 'electron-serve'
import { createWindow } from './helpers/create-window.js'
import fs from 'fs'
const isProd = process.env.NODE_ENV === 'production'

if (isProd) {
  serve({ directory: 'app' })
} else {
  app.setPath('userData', `${app.getPath('userData')} (development)`)
}
ipcMain.on('message', async (event, arg) => {
  event.reply('message', `${arg} World!`)
})

ipcMain.handle("get-med3pa-results", async(event)=>{
  try {
    const INTERNAL_FILE_PATH =  String.raw`C:\Users\thanh\Documents\Work\MEDomics\med3pa\study_3pa\experiments\results\in_hospital_mortality\Internal\MED3paResults_20260525113551.MED3paResults`;
    const data = JSON.parse(fs.readFileSync(INTERNAL_FILE_PATH,'utf8'));
    console.log("message reached backend call")
    return {success:true,data:data};

  } catch(error){
    return {success:false, error:error.messsage}
  }
})
;(async () => {
  await app.whenReady()

  const mainWindow = createWindow('main', {
    width: 1000,
    height: 600,
    webPreferences: {
      preload: path.join(import.meta.dirname, 'preload.js'),
    },
  })
  console.log('preload path:', path.join(import.meta.dirname, 'preload.js'))
  if (isProd) {
    await mainWindow.loadURL('app://./')
  } else {
    const port = process.argv[2]
    await mainWindow.loadURL(`http://localhost:${port}/`)
    mainWindow.webContents.openDevTools()
  }
})()

app.on('window-all-closed', () => {
  app.quit()
})

