module Main where

import Network.HaskellNet.IMAP

import Lib

main :: IO ()
main = do
     conn <- connectIMAPPort "netbook-eth" 8007
     login conn "niege@brain" "secret"
     select conn "INBOX"
     outputAll conn
     mainLoop conn
     putStrLn "Exiting"
