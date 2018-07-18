module Lib
    ( printAndDeleteAll
    , mainLoop
    ) where

import qualified Data.ByteString.Char8 as BS
import Data.String.Utils
import Network.HaskellNet.IMAP
import Network.HaskellNet.IMAP.Connection
import Network.HaskellNet.IMAP.Types

msgToByteString :: [(String, String)] -> BS.ByteString
msgToByteString m = BS.unlines
    [ BS.pack $ strip d
    | (f, d) <- m
    , f == "RFC822.TEXT" ]

printAndDelete :: IMAPConnection -> UID -> IO ()
printAndDelete conn uid = do
    m <- fetchByString conn uid "(RFC822.TEXT)"
    BS.putStr $ msgToByteString m
    store conn uid $ PlusFlags [Seen, Deleted]

printAndDeleteAll conn = do
    search conn [ALLs] >>= mapM (printAndDelete conn)
    expunge conn

mainLoop :: IMAPConnection -> IO ()
mainLoop conn = do
    idle conn 2000
    printAndDeleteAll conn
    mainLoop conn
