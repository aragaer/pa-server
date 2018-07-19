module Lib
    ( mainLoop
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

mainLoop :: IMAPConnection -> IO ()
mainLoop conn = do
    all <- search conn [UNFLAG Deleted]
    if null all
      then idle conn 0
      else mapM_ (printAndDelete conn) all
    expunge conn
    mainLoop conn
