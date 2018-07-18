module Lib
    ( outputAll
    , mainLoop
    ) where

import Control.Monad
import qualified Data.ByteString.Char8 as BS8
import Data.String.Utils
import Network.HaskellNet.IMAP
import Network.HaskellNet.IMAP.Connection
import Network.HaskellNet.IMAP.Types

getText :: [(String, String)] -> [BS8.ByteString]
getText m = do
    (f, d) <- m
    guard (f == "RFC822.TEXT")
    return $ BS8.pack $ strip d

output :: IMAPConnection -> UID -> IO ()
output conn uid = do
    fetchByString conn uid "(RFC822.TEXT)"
        >>= BS8.putStr . BS8.unlines . getText
    store conn uid $ PlusFlags [Seen, Deleted]

outputAll conn = do
    search conn [ALLs] >>= mapM (output conn)
    expunge conn

mainLoop :: IMAPConnection -> IO ()
mainLoop conn = do
    idle conn 2000
    outputAll conn
    mainLoop conn
