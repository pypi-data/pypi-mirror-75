// Copyright (c) 2011-present, Facebook, Inc.  All rights reserved.
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree. An additional grant
// of patent rights can be found in the PATENTS file in the same directory.

#pragma once

#ifndef VIDARDB_LITE

#include <stack>
#include <string>
#include <vector>

#include "utilities/transactions/transaction_util.h"
#include "vidardb/db.h"
#include "vidardb/slice.h"
#include "vidardb/snapshot.h"
#include "vidardb/status.h"
#include "vidardb/types.h"
#include "vidardb/utilities/transaction.h"
#include "vidardb/utilities/transaction_db.h"
#include "vidardb/utilities/write_batch_with_index.h"

namespace vidardb {

class TransactionBaseImpl : public Transaction {
 public:
  TransactionBaseImpl(DB* db, const WriteOptions& write_options);

  virtual ~TransactionBaseImpl();

  void SetSnapshot() override;

  void SetSnapshotOnNextOperation(
      std::shared_ptr<TransactionNotifier> notifier = nullptr) override;

  const Snapshot* GetSnapshot() const override {
    return snapshot_ ? snapshot_.get() : nullptr;
  }

  void ClearSnapshot() override {
    snapshot_.reset();
    snapshot_needed_ = false;
    snapshot_notifier_ = nullptr;
  }

  void SetSavePoint() override;

  Status RollbackToSavePoint() override;

  Status Get(ReadOptions& options, ColumnFamilyHandle* column_family,
             const Slice& key, std::string* value) override;
  Status Get(ReadOptions& options, const Slice& key,
             std::string* value) override {
    return Get(options, db_->DefaultColumnFamily(), key, value);
  }

  Status GetForUpdate(ReadOptions& options, ColumnFamilyHandle* column_family,
                      const Slice& key, std::string* value) override;
  Status GetForUpdate(ReadOptions& options, const Slice& key,
                      std::string* value) override {
    return GetForUpdate(options, db_->DefaultColumnFamily(), key, value);
  }

  Iterator* GetIterator(const ReadOptions& read_options) override;
  Iterator* GetIterator(const ReadOptions& read_options,
                        ColumnFamilyHandle* column_family) override;

  Status Put(ColumnFamilyHandle* column_family, const Slice& key,
             const Slice& value) override;
  Status Put(const Slice& key, const Slice& value) override {
    return Put(nullptr, key, value);
  }

  Status Delete(ColumnFamilyHandle* column_family, const Slice& key) override;
  Status Delete(const Slice& key) override { return Delete(nullptr, key); }

  Status PutUntracked(ColumnFamilyHandle* column_family, const Slice& key,
                      const Slice& value) override;
  Status PutUntracked(const Slice& key, const Slice& value) override {
    return PutUntracked(nullptr, key, value);
  }

  Status DeleteUntracked(ColumnFamilyHandle* column_family,
                         const Slice& key) override;
  Status DeleteUntracked(const Slice& key) override {
    return DeleteUntracked(nullptr, key);
  }

  void PutLogData(const Slice& blob) override;

  void DisableIndexing() override { indexing_enabled_ = false; }
  void EnableIndexing() override { indexing_enabled_ = true; }

  uint64_t GetNumKeys() const override;
  uint64_t GetNumPuts() const override;
  uint64_t GetNumDeletes() const override;

  uint64_t GetElapsedTime() const override;

  WriteBatchWithIndex* GetWriteBatch() override;

  virtual void SetLockTimeout(int64_t timeout) override { /* Do nothing */
  }

  const WriteOptions* GetWriteOptions() override { return &write_options_; }

  void SetWriteOptions(const WriteOptions& write_options) override {
    write_options_ = write_options;
  }

  void UndoGetForUpdate(ColumnFamilyHandle* column_family,
                        const Slice& key) override;
  void UndoGetForUpdate(const Slice& key) override {
    return UndoGetForUpdate(nullptr, key);
  };

  // iterates over the given batch and makes the appropriate inserts.
  // used for rebuilding prepared transactions after recovery.
  Status RebuildFromWriteBatch(WriteBatch* src_batch) override;

  WriteBatch* GetCommitTimeWriteBatch() override;

 protected:
  // Remove pending operations queued in this transaction.
  virtual void Clear();

  void Reinitialize(DB* db, const WriteOptions& write_options);

  // Sets a snapshot if SetSnapshotOnNextOperation() has been called.
  void SetSnapshotIfNeeded();

  // Get list of keys in this transaction that must not have any conflicts
  // with writes in other transactions.
  const TransactionKeyMap& GetTrackedKeys() const { return tracked_keys_; }

  // Helper function to add a key to the given TransactionKeyMap
  static void TrackKey(TransactionKeyMap* key_map, uint32_t cfh_id,
                       const std::string& key, SequenceNumber seqno,
                       bool readonly);

  // Add a key to the list of tracked keys.
  //
  // seqno is the earliest seqno this key was involved with this transaction.
  // readonly should be set to true if no data was written for this key
  void TrackKey(uint32_t cfh_id, const std::string& key, SequenceNumber seqno,
                bool readonly);

  std::unique_ptr<TransactionKeyMap> GetTrackedKeysSinceSavePoint();

  // Called before executing Put, Delete, and GetForUpdate. If TryLock
  // returns non-OK, the Put/Delete/GetForUpdate will be failed.
  // untracked will be true if called from PutUntracked, DeleteUntracked.
  virtual Status TryLock(ColumnFamilyHandle* column_family, const Slice& key,
                         bool read_only, bool untracked = false) = 0;

  // Called when UndoGetForUpdate determines that this key can be unlocked.
  virtual void UnlockGetForUpdate(ColumnFamilyHandle* column_family,
                                  const Slice& key) = 0;

  DB* db_;
  DBImpl* dbimpl_;

  WriteOptions write_options_;

  const Comparator* cmp_;

  // Stores that time the txn was constructed, in microseconds.
  uint64_t start_time_;

  // Stores the current snapshot that was set by SetSnapshot or null if
  // no snapshot is currently set.
  std::shared_ptr<const Snapshot> snapshot_;

  // Count of various operations pending in this transaction
  uint64_t num_puts_ = 0;
  uint64_t num_deletes_ = 0;

  struct SavePoint {
    std::shared_ptr<const Snapshot> snapshot_;
    bool snapshot_needed_;
    std::shared_ptr<TransactionNotifier> snapshot_notifier_;
    uint64_t num_puts_;
    uint64_t num_deletes_;

    // Record all keys tracked since the last savepoint
    TransactionKeyMap new_keys_;

    SavePoint(std::shared_ptr<const Snapshot> snapshot, bool snapshot_needed,
              std::shared_ptr<TransactionNotifier> snapshot_notifier,
              uint64_t num_puts, uint64_t num_deletes)
        : snapshot_(snapshot),
          snapshot_needed_(snapshot_needed),
          snapshot_notifier_(snapshot_notifier),
          num_puts_(num_puts),
          num_deletes_(num_deletes) {}
  };

 private:
  // Records writes pending in this transaction
  WriteBatchWithIndex write_batch_;

  // batch to be written at commit time
  WriteBatch commit_time_batch_;

  // Stack of the Snapshot saved at each save point. Saved snapshots may be
  // nullptr if there was no snapshot at the time SetSavePoint() was called.
  std::unique_ptr<std::stack<TransactionBaseImpl::SavePoint>> save_points_;

  // Map from column_family_id to map of keys that are involved in this
  // transaction.
  // Pessimistic Transactions will do conflict checking before adding a key
  // by calling TrackKey().
  TransactionKeyMap tracked_keys_;

  // If true, future Put/Deletes will be indexed in the WriteBatchWithIndex.
  // If false, future Put/Deletes will be inserted directly into the
  // underlying WriteBatch and not indexed in the WriteBatchWithIndex.
  bool indexing_enabled_;

  // SetSnapshotOnNextOperation() has been called and the snapshot has not yet
  // been reset.
  bool snapshot_needed_ = false;

  // SetSnapshotOnNextOperation() has been called and the caller would like
  // a notification through the TransactionNotifier interface
  std::shared_ptr<TransactionNotifier> snapshot_notifier_ = nullptr;

  WriteBatchBase* GetBatchForWrite();

  // Used for memory management for snapshot_
  void ReleaseSnapshot(const Snapshot* snapshot, DB* db);

  void SetSnapshotInternal(const Snapshot* snapshot);
};

}  // namespace vidardb

#endif  // VIDARDB_LITE
