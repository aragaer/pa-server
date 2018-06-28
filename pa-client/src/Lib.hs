module Lib
    ( output
    , outputAll
    , mainLoop
    ) where

import Data.Text
import Data.Text.Encoding
import Network.HaskellNet.IMAP
import Network.HaskellNet.IMAP.Connection
import Network.HaskellNet.IMAP.Types


output :: IMAPConnection -> UID -> IO ()
output conn uid = do
       msg <- fetch conn uid
       putStr $ unpack $ decodeUtf8 msg
       store conn uid $ PlusFlags [Seen, Deleted]

outputAll :: IMAPConnection -> IO ()
outputAll conn = do
     found <- search conn [ALLs]
     mapM (output conn) found
     expunge conn
     return ()

mainLoop :: IMAPConnection -> IO ()
mainLoop conn = do
     idle conn 10000
     outputAll conn
     mainLoop conn
