module Main where

import Network.HaskellNet.IMAP
import System.Environment
import System.IO

import Lib

main :: IO ()
main = do
     hSetBuffering stdout LineBuffering
     args <- getArgs
     conn <- connectIMAPPort (args!!0) $ read (args!!1)
     login conn (args!!2) (args!!3)
     select conn "INBOX"
     printAndDeleteAll conn
     mainLoop conn
     putStrLn "Exiting"
