// Copyright 2015, 2016 Ethcore (UK) Ltd.
// This file is part of Parity.

// Parity is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// Parity is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with Parity.  If not, see <http://www.gnu.org/licenses/>.

export function statusBlockNumber (blockNumber) {
  return {
    type: 'statusBlockNumber',
    blockNumber
  };
}

export function statusCollection (collection) {
  return {
    type: 'statusCollection',
    collection
  };
}

export function statusLogs (logInfo) {
  return {
    type: 'statusLogs',
    logInfo
  };
}

export function toggleStatusLogs (devLogsEnabled) {
  return {
    type: 'toggleStatusLogs',
    devLogsEnabled
  };
}

export function clearStatusLogs () {
  return {
    type: 'clearStatusLogs'
  };
}

export function toggleStatusRefresh (refreshStatus) {
  return {
    type: 'toggleStatusRefresh',
    refreshStatus
  };
}
